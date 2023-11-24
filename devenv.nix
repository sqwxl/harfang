{ pkgs, ... }:

{
  name = "Harfang";

  packages = [
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
      djlint = {
        enable = true;
        name = "djlint-reformat-django";
        files = ".*/templates/.*\.html$";
        entry = "${pkgs.djlint}/bin/djlint --reformat --profile=django";
      };
    };
  };
}
