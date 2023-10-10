{ pkgs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = [
    pkgs.just
    pkgs.black
  ];

  enterShell = ''
    python --version
  '';

  # https://devenv.sh/languages/
  languages.python.enable = true;
  languages.python.venv.enable = true;
  languages.python.version = "3.11.5";

  # https://devenv.sh/pre-commit-hooks/
  pre-commit.hooks = {
    autoflake.enable = true;
    black.enable = true;
    flake8.enable = true;
    flynt = {
      enable = true;
      name = "flynt";
      files = ".*\.py";
      entry = "${pkgs.python311Packages.flynt}/bin/flynt --fail-on-change";
    };
    isort.enable = true;
    nixpkgs-fmt.enable = true;
    pyupgrade.enable = true;
    ruff.enable = true;
    djhtml = {
      enable = true;
      name = "djhtml";
      files = ".*/templates/.*\.html$";
      entry = "${pkgs.djhtml}/bin/djhtml";
    };
  };

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";

  # See full reference at https://devenv.sh/reference/options/
}
