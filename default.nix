let
  pkgs = import (builtins.fetchGit {
    url = "https://github.com/nixos/nixpkgs/";
    ref = "refs/heads/nixos-unstable";
    rev = "b8697e57f10292a6165a20f03d2f42920dfaf973"; # 4-03-2024
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs nixos-unstable`
  }) { config = {}; };
  pythonCore = pkgs.python311;
  pythonPkgs = python-packages: with python-packages; [
      google_api_python_client
      google-auth-oauthlib

      pytest
    ]; 
  myPython = pythonCore.withPackages pythonPkgs;
in
{
  shell = pkgs.mkShellNoCC {
    buildInputs = with pkgs; [
      git
      gnumake
      myPython
      pyright
      ruff
      ruff-lsp
    ];
  };
}
