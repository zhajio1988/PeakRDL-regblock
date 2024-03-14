from typing import List
import subprocess
import os
import shutil

from .base import Simulator
import shlex
class vcs(Simulator):
    name = "vcs"

    @classmethod
    def is_installed(cls) -> bool:
        print("debug point ", shutil.which("vcs"))
        return (
            shutil.which("vcs") is not None
        )

    def compile(self) -> None:
        cmd = [
            "bsub -Is vcs", " -l", " build.log",

            " -sverilog +v2k +vcs+fsdbon +vcs+lic+wait -timescale=1ns/1ns -kdb -lca -debug_access+all -full64"

            " +incdir+%s" % os.path.join(os.path.dirname(__file__), ".."),

            " -top tb"
        ]

        # Add source files
        cmd.extend(self.tb_files)

        # Run command!
        print("debug point cmd", shlex.split(" ".join(cmd)))
        subprocess.run(shlex.split(" ".join(cmd)), check=True)


    def run(self, plusargs:List[str] = None) -> None:
        plusargs = plusargs or []

        test_name = self.testcase.request.node.name

        # call vsim
        cmd = [
            "bsub -Is ./simv -l %s.log  +fsdb+all=on +fsdbfile+test.fsdb" % test_name,
        ]

        for plusarg in plusargs:
            cmd.append("+" + plusarg)
        subprocess.run(shlex.split(" ".join(cmd)), check=True)

        self.assertSimLogPass("%s.log" % test_name)

    def assertSimLogPass(self, path: str):
        self.testcase.assertTrue(os.path.isfile(path))

        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("# ** Error"):
                    self.testcase.fail(line)
                elif line.startswith("# ** Fatal"):
                    self.testcase.fail(line)
