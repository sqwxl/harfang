{ pkgs, ... }:

{
  name = "Harfang";

  packages = [
    pkgs.djhtml
    pkgs.djlint
    pkgs.gettext
    pkgs.just
    pkgs.marksman
    pkgs.pyright
    pkgs.ruff-lsp
    pkgs.tailwindcss
  ];

  languages.python.enable = true;
  languages.python.venv.enable = true;
  languages.python.venv.requirements = "-r ${./requirements.txt}";

  difftastic.enable = true;

  pre-commit = {
    excludes = [
      ".*/migrations/.*"
    ];
    hooks = {
      nixpkgs-fmt.enable = true;
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
