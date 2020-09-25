let
  nixpkgs = builtins.fetchGit {
    name = "nixos-unstable-2020-05-9";
    url = "https://github.com/nixos/nixpkgs-channels/";
    ref = "refs/heads/nixos-unstable";
    rev = "46f975f81e0f71ba0d2b2bb8fe4006a9aa4c6c5c";
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs-channels nixos-unstable`
  };
in
  import nixpkgs { config = {}; }
