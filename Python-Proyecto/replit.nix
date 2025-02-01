{ pkgs }: {
  deps = [
    pkgs.haskellPackages.hsakamai
    pkgs.wget
    pkgs.openssh
    pkgs.nano
    pkgs.non
    pkgs.libosmscout
    pkgs.chromedriver
    pkgs.chromium
  ];
}