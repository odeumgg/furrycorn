{ bootFetchgit ? (import <nixpkgs> {}).fetchgit }:
let
  pkgs = import (bootFetchgit (import ./z/etc/versions/nixpkgs.nix)) {};
  inherit (pkgs) stdenv callPackage;

  pythonPkg = callPackage ./z/etc/python/requirements.nix {};
in pythonPkg
