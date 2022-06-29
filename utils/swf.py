import os
from pathlib import Path
from typing import List, Dict, Any

from constants import DEFAULT_SWF

class SwfJob(object):
    """Format as specified in
       http://www.cs.huji.ac.il/labs/parallel/workload/swf.html
    """

    def __init__(self,
                 job_id,
                 submit_time,
                 wait_time,
                 run_time,
                 allocated_cores,
                 mips_per_core):
        self._job_id = job_id
        self._submit_time = submit_time
        self._wait_time = wait_time
        self._run_time = run_time
        self._allocated_cores = allocated_cores
        self._mips_per_core = mips_per_core

    @property
    def mips_per_core(self):
        return self._mips_per_core

    @property
    def job_id(self):
        return self._job_id

    @property
    def submit_time(self):
        return self._submit_time

    @property
    def wait_time(self):
        return self._wait_time

    @property
    def run_time(self):
        return self._run_time

    @property
    def allocated_cores(self):
        return self._allocated_cores

    def as_cloudlet_descriptor_dict(self):
        return {
            'jobId': self.job_id,
            'submissionDelay': self.submit_time,
            'mi': self.run_time * self.mips_per_core * self.allocated_cores,
            'numberOfCores': self._allocated_cores,
        }


def read_swf(swf_resource: (str, str) = DEFAULT_SWF) -> List[Dict[str, Any]]:

    jobs = []
    filename, url = swf_resource
    filename = "data/" + filename

    # download and unzip swf file if not existent
    if not Path(filename).exists():
        from utils.utils import download_from_url
        gz_filename = filename + ".gz"
        download_from_url(url, gz_filename)

        import gzip
        import shutil
        with gzip.open(gz_filename, 'rb') as f_in:
            with open(filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(Path(gz_filename))

    # read swf file and create jobs
    with open(filename, 'r') as f:
        for _ in range(1):
            next(f)
        for line in f.readlines():
            if line.startswith(';'):
                continue

            stripped = line.strip()
            splitted = stripped.split()

            job_id = splitted[0]
            submit_time = float(splitted[1])
            wait_time = float(splitted[2])
            run_time = splitted[3]
            allocated_cores = splitted[4]

            mips = 1250

            if int(run_time) > 0 and int(allocated_cores) > 0:
                job = SwfJob(
                    job_id=int(job_id),
                    submit_time=int(submit_time),
                    wait_time=int(wait_time),
                    run_time=int(run_time),
                    allocated_cores=int(allocated_cores),
                    mips_per_core=int(mips),
                )
                jobs.append(job.as_cloudlet_descriptor_dict())
    return jobs
