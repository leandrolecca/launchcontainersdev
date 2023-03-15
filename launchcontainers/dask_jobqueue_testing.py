import dask
from dask.distributed import Client
from dask_jobqueue import PBSCluster, SGECluster, SLURMCluster
import time
from dask.distributed import progress
def slow_it(x):
    time.sleep(1)
    return x+1

def main():
    
    cluster_sge= SGECluster(cores  = 6, memory= "32GB",
                    queue="long.q",
                    name = "test_how_this_work",
                    )
    
    cluster_sge.scale(20)

    client = Client(cluster_sge)

    
    print(f"--------this is cluster job script {cluster_sge.job_script}")

    future=client.map(slow_it, range(1000))
    progress(future)
    print(f"------------lenth of future is {len(future)}")
    results=client.gather(future)
    print(f"----this is result:   {type(results)}\n -------{results}")
    return

if __name__ == "__main__":
    main()
   
