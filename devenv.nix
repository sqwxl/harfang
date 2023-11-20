{ pkgs, ... }:

{
  name = "Harfang";

  env.GREET = "devenv";

  packages = [
    pkgs.just
    pkgs.djhtml
  ];

  languages.python.enable = true;
  languages.python.venv.enable = true;

  pre-commit = {
    excludes = [
      ".*/migrations/.*"
    ];
    hooks = {
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
  };
}
