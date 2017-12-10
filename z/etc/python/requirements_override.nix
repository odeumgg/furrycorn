{ pkgs, python }:

self: super: {
  "jsonschema" = python.overrideDerivation super."jsonschema" (old: {
    preConfigure = ''
      sed -i -e "s|setup_requires=\[.*\],|setup_requires=\[\],|" setup.py  
    '';
  });
}
