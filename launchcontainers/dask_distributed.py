import dask
from dask.distributed import Client
from dask_jobqueue import PBSCluster, SGECluster, SLURMCluster

# define the sge cluster
cluster_sge= SGECluster(cores  = 6, memory= "32GB",
                    queue="long.q",
                    job_extra=[],
                    name = "test_how_this_work",
                    worker_name="this is worker", 
                    )
client = Client(cluster_sge)

