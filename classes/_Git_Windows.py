import shlex
import subprocess as sp
import platform
from typing import AnyStr, List, NamedTuple, Optional, Union


if 'windows' not in platform.platform().lower():
    raise NotImplementedError("Use the `sh` module's `git` from PyPI instead!")


ProcReturn = NamedTuple('ProcReturn', [('stdout', str), ('stderr', str), ('code', int)])

GitError = sp.CalledProcessError


def _call_process(execcmd: AnyStr, _ok_code: Union[int, List[int]] = None, return_data: bool = False) -> \
        Optional[ProcReturn]:
    proc = sp.Popen(shlex.split(execcmd), stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    (stdout, stderr) = proc.communicate()
    retcode = proc.returncode
    if retcode != 0:
        if _ok_code and retcode in _ok_code:
            pass
        else:
            raise GitError(retcode, execcmd, stdout, stderr)

    if return_data:
        return ProcReturn(stdout, stderr, retcode)


class Git:
    # add
    @staticmethod
    def add(*args: str) -> None:
        execcmd = "git add " + " ".join(args)
        _call_process(execcmd)

    # branch
    @staticmethod
    def branch(*args: str) -> None:
        execcmd = "git branch " + " ".join(args)
        _call_process(execcmd)

    # Checkout
    @staticmethod
    def checkout(*args: str) -> None:
        execcmd = "git checkout " + " ".join(args)
        _call_process(execcmd)

    # commit
    @staticmethod
    def commit(*args: str) -> None:
        execcmd = "git commit " + " ".join(args)
        _call_process(execcmd)

    # Config
    @staticmethod
    def config(*args: str, _ok_code: int = 0) -> None:
        execcmd = "git config " + " ".join(args)
        _call_process(execcmd, _ok_code=_ok_code)

    # merge
    @staticmethod
    def merge(*args: str) -> None:
        execcmd = "git merge " + " ".join(args)
        _call_process(execcmd)

    # fetch
    @staticmethod
    def fetch(*args: str) -> None:
        execcmd = "git fetch " + " ".join(args)
        _call_process(execcmd)

    # pull
    @staticmethod
    def pull(*args: str) -> None:
        execcmd = "git pull " + " ".join(args)
        _call_process(execcmd)

    # push
    @staticmethod
    def push(*args: str) -> None:
        execcmd = "git push " + " ".join(args)
        _call_process(execcmd)

    # remote.update
    class remote:  # noqa: N801
        @staticmethod
        def update(*args: str) -> None:
            execcmd = "git remote update " + " ".join(args)
            _call_process(execcmd)

    # reset
    @staticmethod
    def reset(*args: str) -> None:
        execcmd = "git reset " + " ".join(args)
        _call_process(execcmd)

    # rev-parse
    @staticmethod
    def rev_parse(*args: str) -> str:
        execcmd = "git rev-parse " + " ".join(args)
        return _call_process(execcmd, return_data=True).stdout

    # status
    @staticmethod
    def status(*args: str) -> str:
        execcmd = "git status " + " ".join(args)
        return _call_process(execcmd, return_data=True).stdout

    # status with colours stripped
    @staticmethod
    def status_stripped(*args: str) -> str:
        execcmd = "git -c color.status=false status " + " ".join(args)
        return _call_process(execcmd, return_data=True).stdout

    # diff
    @staticmethod
    def diff(*args: str) -> str:
        execcmd = "git diff " + " ".join(args)
        return _call_process(execcmd, return_data=True).stdout

    # diff with colours stripped, filenames only
    @staticmethod
    def diff_filenames(*args: str) -> str:
        execcmd = "git -c color.diff=false diff --name-only " + " ".join(args)
        return _call_process(execcmd, return_data=True).stdout
