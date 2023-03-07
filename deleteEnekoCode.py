def pySPFM(
    data_fn,
    mask_fn,
    output_filename,
    tr,
    out_dir=".",
    te=[0],
    hrf_model="spm",
    block_model=False,
    debias=True,
    group=0.2,
    criterion="bic",
    pcg=0.8,
    factor=10,
    lambda_echo=-1,
    max_iter_factor=1.0,
    max_iter_fista=500,
    max_iter_spatial=100,
    max_iter=10,
    min_iter_fista=50,
    jobqueue=None,
    n_jobs=4,
    spatial_weight=0,
    spatial_lambda=1,
    spatial_dim=3,
    mu=0.01,
    tolerance=1e-6,
    use_bids=False,
    n_surrogates=50,
    debug=False,
    quiet=False,
    command_str=None,
):
    """pySPFM is a Python programm for the Sparse Paradigm Free Mapping algorithm.
    Parameters
    ----------
    data_fn : str
        Input data file(s). List of files for multi-echo data
    mask_fn : str
        Input mask file
    output_filename : str
        Prefix of output files.
    tr : float
        Repetition time
    out_dir : str
        Output directory
    te : list, optional
        TE values in ms, by default [0], i.e. single-echo
    hrf_model : str, optional
        HRF model to use, by default 'spm', i.e. SPM's canonical HRF.
        Options are 'spm', 'glover' and a path to a 1D file with a custom HRF model.
    block_model : bool, optional
        Use the block model instead of using the spike model, by default False
    debias : bool, optional
        Perform debiasing step to recover true amplitude of estimates, by default True
    group : float, optional
        Grouping (l2,1-norm) regularization parameter, by default 0.2
    criterion : str, optional
        Criterion to select regularization parameter lambda, by default "bic"
    pcg : float, optional
        Percentage of the maximum lambda possible to use as lambda, by default 0.8
    factor : int, optional
        Factor of the estimate of the level of noise to use as lambda, by default 10
    lambda_echo : int, optional
        When using multi-echo data, the number of TE to use to estimate the level of the noise,
        by default -1
    max_iter_factor : float, optional
        Percentage of TRs to limit the LARS search to (less is faster), by default 1.0
    max_iter_fista : int, optional
        Maximum number of iterations for FISTA, by default 500
    max_iter_spatial : int, optional
        Maximum number of iterations for spatial regularization, by default 100
    max_iter : int, optional
        Maximum number of iterations to solve both temporal and spatial regularization,
        by default 10
    min_iter_fista : int, optional
        Minimum number of iterations for FISTA, by default 50
    jobqueue : str, optional
        Jobqueue to use for parallel processing, by default None
    n_jobs : int, optional
        Number of parallel jobs to use on for loops, by default 4
    spatial_weight : int, optional
        Weighting between the temporal and spatial regularization, by default 0 (only temporal)
    spatial_lambda : int, optional
        Regularization parameter for spatial regularization, by default 1
    spatial_dim : int, optional
        Dimensions of the spatial regularization filter (can be 2 for slices or 3 for volume),
        by default 3
    mu : float, optional
        Step size for spatial regularization, by default 0.01
    tolerance : float, optional
        Tolerance for residuals to find convergence of inverse problem, by default 1e-6
    is_atlas : bool, optional
        Read mask as atlas with different labels, by default False
    use_bids : bool, optional
        Use BIDS-style suffix on the given `output` (default = False). pySPFM assumes that `output`
        follows the BIDS convention. Not using this option will default to using AFNI to update the
        header of the output."
    n_surrogates : int, optional
        Number of surrogates to generate for stability selection, by default 50
    debug : bool, optional
        Logger option for debugging, by default False
    quiet : bool, optional
        Quiet logger option (no messages shown), by default False
    command_str : str, optional
        Command string to be used in the log file, by default None.
    Raises
    ------
    ValueError
        If wrong criterion is provided.
    """
    # Generate output directory if it doesn't exist
    out_dir = op.abspath(out_dir)
    if not op.isdir(out_dir):
        os.mkdir(out_dir)

    # Save command into sh file, if the command-line interface was used
    if command_str is not None:
        command_file = open(os.path.join(out_dir, "call.sh"), "w")
        command_file.write(command_str)
        command_file.close()

    LGR = logging.getLogger("GENERAL")
    # RefLGR = logging.getLogger("REFERENCES")
    # create logfile name
    basename = "pySPFM_"
    extension = "tsv"
    start_time = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    logname = op.join(out_dir, (basename + start_time + "." + extension))
    refname = op.join(out_dir, "_references.txt")
    utils.setup_loggers(logname, refname, quiet=quiet, debug=debug)

    LGR.info("Using output directory: {}".format(out_dir))

    n_te = len(te)

    if all(i >= 1 for i in te):
        te = [x / 1000 for x in te]

    LGR.info("Reading data...")
    if n_te == 1:
        data_masked, masker = read_data(data_fn[0], mask_fn)
        n_scans = data_masked.shape[0]
        n_voxels = data_masked.shape[1]
    elif n_te > 1:
        # If the first element of data_fn has spaces, it is a list of paths
        # Convert it into a list
        if " " in data_fn[0]:
            data_fn = data_fn[0].split(" ")

        for te_idx in range(n_te):
            data_temp, masker = read_data(data_fn[te_idx], mask_fn)
            if te_idx == 0:
                data_masked = data_temp
                n_scans = data_temp.shape[0]
                n_voxels = data_temp.shape[1]
            else:
                # data_temp, _, _, _ = read_data(data_fn[te_idx], mask_fn, mask_idxs)
                data_masked = np.concatenate((data_masked, data_temp), axis=0)

            LGR.info(f"{te_idx + 1}/{n_te} echoes...")

    LGR.info("Data read.")

    # Generate design matrix with shifted versions of HRF
    LGR.info("Generating design matrix with shifted versions of HRF...")
    hrf_obj = hrf_generator.HRFMatrix(te=te, block=block_model, model=hrf_model)
    hrf = hrf_obj.generate_hrf(tr=tr, n_scans=n_scans).hrf_

    # Run LARS if bic or aic on given.
    # If another criterion is given, then solve with FISTA.
    lars_criteria = ["bic", "aic"]
    fista_criteria = ["mad", "mad_update", "ut", "lut", "factor", "pcg", "eigval"]

    # Run for loop only once for just temporal regularization
    if spatial_weight == 0:
        max_iter = 1
    else:
        # Initialize variables for spatial regularization
        estimates_temporal = np.empty((n_scans, n_voxels))
        estimates_spatial = np.empty((n_scans, n_voxels))
        final_estimates = np.empty((n_scans, n_voxels))

    # Initialize list to save keywords used for BIDS compatible outputs
    out_bids_keywords = []

    # Iterate between temporal and spatial regularizations
    client, _ = dask_scheduler(n_jobs, jobqueue)

    # Scatter data to workers if client is not None
    if client is not None:
        hrf_fut = client.scatter(hrf)
    else:
        hrf_fut = hrf

    # Solve stability selection
    if criterion == "stability":
        LGR.info("Solving inverse problem with stability selection...")
        n_lambdas = int(np.ceil(max_iter_factor * n_scans))
        auc = np.zeros((n_scans, n_voxels))

        # Solve stability regularization
        futures = [
            delayed_dask(stability_selection.stability_selection)(
                hrf_fut,
                data_masked[:, vox_idx],
                n_lambdas,
                n_surrogates,
            )
            for vox_idx in range(n_voxels)
        ]

        # Gather results
        if client is not None:
            stability_estimates = compute(futures)[0]
        else:
            stability_estimates = compute(futures, scheduler="single-threaded")[0]

        for vox_idx in range(n_voxels):
            auc[:, vox_idx] = np.squeeze(stability_estimates[vox_idx])

        LGR.info("Stability selection finished.")

        LGR.info("Saving AUCs to %s..." % out_dir)
        out_bids_keywords.append("AUC")
        output_name = get_outname(output_filename, "AUC", "nii.gz", use_bids)
        write_data(
            auc,
            os.path.join(out_dir, output_name),
            masker,
            data_fn[0],
            command_str,
            use_bids,
        )

    # Solve FISTA
    else:
        for iter_idx in range(max_iter):
            if spatial_weight > 0:
                data_temp_reg = final_estimates - estimates_temporal + data_masked
            else:
                data_temp_reg = data_masked

            estimates = np.zeros((n_scans, n_voxels))
            lambda_map = np.zeros(n_voxels)

            if criterion in lars_criteria:
                LGR.info("Solving inverse problem with LARS...")
                n_lambdas = int(np.ceil(max_iter_factor * n_scans))
                # Solve LARS for each voxel with parallelization
                futures = []
                for vox_idx in range(n_voxels):
                    fut = delayed_dask(lars.solve_regularization_path, pure=False)(
                        hrf_fut, data_temp_reg[:, vox_idx], n_lambdas, criterion
                    )
                    futures.append(fut)

                # Gather results
                if client is not None:
                    lars_estimates = compute(futures)[0]
                else:
                    lars_estimates = compute(futures, scheduler="single-threaded")[0]

                for vox_idx in range(n_voxels):
                    estimates[:, vox_idx] = np.squeeze(lars_estimates[vox_idx][0])
                    lambda_map[vox_idx] = np.squeeze(lars_estimates[vox_idx][1])

            elif criterion in fista_criteria:
                LGR.info("Solving inverse problem with FISTA...")
                # Solve fista
                futures = []
                for vox_idx in range(n_voxels):
                    fut = delayed_dask(fista.fista, pure=False)(
                        hrf_fut,
                        data_temp_reg[:, vox_idx],
                        criterion=criterion,
                        max_iter=max_iter_fista,
                        min_iter=min_iter_fista,
                        tol=tolerance,
                        group=group,
                        pcg=pcg,
                        factor=factor,
                        lambda_echo=lambda_echo,
                    )
                    futures.append(fut)

                # Gather results
                if client is not None:
                    fista_estimates = compute(futures)[0]
                else:
                    fista_estimates = compute(futures, scheduler="single-threaded")[0]

                for vox_idx in range(n_voxels):
                    estimates[:, vox_idx] = np.squeeze(fista_estimates[vox_idx][0])
                    lambda_map[vox_idx] = np.squeeze(fista_estimates[vox_idx][1])

            else:
                raise ValueError("Wrong criterion option given.")

            # Convolve with HRF
            if block_model:
                estimates_block = estimates
                hrf_obj = hrf_generator.HRFMatrix(te=te, block=False, model=hrf_model)
                hrf_fitting = hrf_obj.generate_hrf(tr=tr, n_scans=n_scans).hrf_
                estimates_spike = np.dot(np.tril(np.ones(n_scans)), estimates_block)
                fitts = np.dot(hrf_fitting, estimates_spike)
            else:
                estimates_spike = estimates
                fitts = np.dot(hrf, estimates_spike)

            # Perform spatial regularization if a weight is given
            if spatial_weight > 0:
                # Update temporal estimates
                estimates_temporal = estimates_temporal + (estimates - final_estimates)

                # Calculates for the whole volume
                estimates_tikhonov = spatial_regularization.spatial_tikhonov(
                    final_estimates,
                    final_estimates - estimates_spatial + data_masked,
                    masker,
                    max_iter_spatial,
                    spatial_dim,
                    spatial_lambda,
                    mu,
                )

                # Update spatial estimates
                estimates_spatial = estimates_spatial + (estimates_tikhonov - final_estimates)

                # Calculate final estimates
                final_estimates = (
                    estimates_temporal * (1 - spatial_weight) + spatial_weight * estimates_spatial
                )
            else:
                final_estimates = estimates

        LGR.info("Inverse problem solved.")

        # Update HRF for block model
        if block_model:
            hrf_obj = hrf_generator.HRFMatrix(te=te, block=False, model=hrf_model)
            hrf = hrf_obj.generate_hrf(tr=tr, n_scans=n_scans).hrf_

        # Perform debiasing step
        if debias:
            LGR.info("Debiasing estimates...")
            if block_model:
                estimates_spike = debiasing.debiasing_block(
                    hrf=hrf, y=data_masked, estimates_matrix=final_estimates
                )
                fitts = np.dot(hrf, estimates_spike)
            else:
                estimates_spike, fitts = debiasing.debiasing_spike(
                    hrf, data_masked, final_estimates
                )
        elif block_model:
            estimates_spike = np.dot(np.tril(np.ones(n_scans)), estimates_block)
            fitts = np.dot(hrf, estimates_spike)

        LGR.info("Saving results...")

        # Save innovation signal
        if block_model:
            estimates_block = final_estimates
            output_name = get_outname(output_filename, "innovation", "nii.gz", use_bids)
            out_bids_keywords.append("innovation")
            write_data(
                estimates_block,
                os.path.join(out_dir, output_name),
                masker,
                data_fn[0],
                command_str,
                use_bids=use_bids,
            )

            if not debias:
                hrf_obj = hrf_generator.HRFMatrix(TR=tr, n_scans=n_scans, TE=te, block=False)
                hrf = hrf_obj.generate_hrf().hrf
                estimates_spike = np.dot(np.tril(np.ones(n_scans)), estimates_block)
                fitts = np.dot(hrf, estimates_spike)

        # Save activity-inducing signal
        if n_te == 1:
            output_name = get_outname(output_filename, "activityInducing", "nii.gz", use_bids)
            out_bids_keywords.append("activityInducing")
        elif n_te > 1:
            output_name = get_outname(output_filename, "activityInducing", "nii.gz", use_bids)
            out_bids_keywords.append("activityInducing")
        write_data(
            estimates_spike,
            os.path.join(out_dir, output_name),
            masker,
            data_fn[0],
            command_str,
            use_bids=use_bids,
        )

        # Save fitts
        if n_te == 1:
            output_name = get_outname(output_filename, "denoised_bold", "nii.gz", use_bids)
            out_bids_keywords.append("denoised_bold")
            write_data(
                fitts,
                os.path.join(out_dir, output_name),
                masker,
                data_fn[0],
                command_str,
                use_bids=use_bids,
            )
        elif n_te > 1:
            for te_idx in range(n_te):
                te_data = fitts[te_idx * n_scans : (te_idx + 1) * n_scans, :]
                output_name = get_outname(
                    f"{output_filename}_echo-{te_idx + 1}", "denoised_bold", "nii.gz", use_bids
                )
                out_bids_keywords.append(f"echo-{te_idx + 1}_desc-denoised_bold")
                write_data(
                    te_data,
                    os.path.join(out_dir, output_name),
                    masker,
                    data_fn[0],
                    command_str,
                    use_bids=use_bids,
                )

        # Save noise estimate
        if n_te == 1:
            output_name = get_outname(output_filename, "MAD", "nii.gz", use_bids)
            out_bids_keywords.append("MAD")
            out_data = data_masked[:n_scans, :]
            _, _, noise_estimate = select_lambda.select_lambda(hrf=hrf, y=out_data)
            write_data(
                np.expand_dims(noise_estimate, axis=0),
                os.path.join(out_dir, output_name),
                masker,
                data_fn[0],
                command_str,
                use_bids=use_bids,
            )
        else:
            for te_idx in range(n_te):
                output_name = get_outname(
                    output_filename, f"echo-{te_idx + 1}_MAD", "nii.gz", use_bids
                )
                out_bids_keywords.append(f"echo-{te_idx + 1}_MAD")
                if te_idx == 0:
                    y_echo = data_masked[:n_scans, :]
                else:
                    y_echo = data_masked[te_idx * n_scans : (te_idx + 1) * n_scans, :]
                _, _, noise_estimate = select_lambda.select_lambda(hrf=hrf, y=y_echo)
                write_data(
                    np.expand_dims(noise_estimate, axis=0),
                    os.path.join(out_dir, output_name),
                    masker,
                    data_fn[0],
                    command_str,
                    use_bids=use_bids,
                )

        # Save lambda
        out_keyword = "lambda"
        if use_bids:
            out_keyword = f"stat-{out_keyword}_statmap"
        output_name = get_outname(output_filename, out_keyword, "nii.gz", use_bids)
        out_bids_keywords.append(out_keyword)
        write_data(
            np.expand_dims(lambda_map, axis=0),
            os.path.join(out_dir, output_name),
            masker,
            data_fn[0],
            command_str,
            use_bids=use_bids,
        )

    # Save BIDS compatible sidecar file
    if use_bids:
        write_json(out_bids_keywords, out_dir)

    LGR.info("Results saved.")

    LGR.info("pySPFM finished.")
    utils.teardown_loggers()