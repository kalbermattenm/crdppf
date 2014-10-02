CRDPPF Portal
============

# Getting started

  
Checkout the source code:

    $ git clone https://github.com/SIT-Jura/crdppf.git

or when you're using ssh key (see https://help.github.com/articles/generating-ssh-keys):

    $ git clone git@github.com:SIT-Jura/crdppf.git

Get the submodule crdppf_core (https://github.com/SIT-Jura/crdppf_core.git if you'd like to get the core project too)

    $ git submodule update --init
    
Once it is installed get all the libraries of the submodule (ext, openlayers, ...)

    $ cd crdppf_core
    $ git submodule update --init
     
maybe a 

    $ git submodule foreach git submodule update --init

Bootstrap and buildout

    $ python bootstrap.py --version 1.5.2 --distribute --download-base \
        http://pypi.camptocamp.net/distribute-0.6.22_fix-issue-227/ --setup-source \
        http://pypi.camptocamp.net/distribute-0.6.22_fix-issue-227/distribute_setup.py

After the installation put the directoriy crdpp in W

    $ cd ..
    $ chmod -R o+w crdppf


does also the trick
Create your own buildout file by:
* Copy-paste `buildout.cfg`
* Rename the new file `buildout_<user>.cfg`
* Open this file in a text editor
* Erase all sections except the `[vars]` section
* In the `[vars]` section, delete all lines which do not contain `overwrite_me`
* At the top of the file, add the extend instruction:

```
[buildout]
extends = buildout.cfg
```

Adapt the `overwrite_me` values to your environment:
* `mapproxyurl` has to be a single or a list of WMTS URLs (like 'http://wmts1', 'http://wmts2', ...)
* If you do not set `proxy_enabled` to True, then you do not need to set the four remaining (`proxy_user`, `proxy_pass`, `proxy_server`, `proxy_port`).

Run buildout

    $ ./buildout/bin/buildout -c buildout_<user>.cfg

# Change in crdppf_core (not in variable)
Changement a effectuer dans crdppf_core en attendant que cela passe en variable dans le projet NE

crdppf/crdppf_core/crdppf/static/js/Crdppf/main.js

    $ center: new OpenLayers.LonLat(583000, 243000),
    
crdppf/crdppf_core/crdppf/static/js/Crdppf/map.js
    $ resolutions: [350,140,70,26.5,14,7,3.5,2.65,1.75,1.3,0.7,0.35,0.2,0.1,0.05],
    $ 
    $ maxExtent: new OpenLayers.Bounds(420000.0, 30000.0, 900000.0, 350000.0),
    $ 
    $ restrictedExtent: new OpenLayers.Bounds , et y metre les coord JU (530000,200000,630000,285000)
    $ 
    $     var overviewMap = new OpenLayers.Control.OverviewMap({
    $             layers: [
    $                 new OpenLayers.Layer.Image(
    $                     "overview",
    $                     Crdppf.staticImagesDir + 'overviewmap.png',
    $                     new OpenLayers.Bounds(554000, 220000, 610000, 262000),
    $                     new OpenLayers.Size(147, 110)
    $                 )
    $             ],
    $             size: new OpenLayers.Size(147, 110),
    $             maximized: true,
    $ 
         
crdppf/crdppf_core/crdppf/templates/derived/globals.js        
    $ 'plan_cadastral_name': 'plan_cadastral${request.tile_date[0]}'

crdppf/crdppf_core/crdppf/util/pdf_classes.py
    Lignes 113 et 247, remplacer \Placeholder.jpg par
    $ /Placeholder.jpg
    Ligne 83
    $ self.cantonlogopath = 'ecussons/JUcompactrvb.jpg’
    Ligne 109
    $ self.image(self.appconfig.imagesbasedir+self.pdfconfig.cantonlogopath, 110, 8, 44.0, 9.5)
    Ligne 243
    $ self.image(self.appconfig.imagesbasedir+self.pdfconfig.cantonlogopath, 110, 8, 44.0, 9.5)

crdppf/crdppf_core/crdppf/util/table2model_match.py
    Remplacer 
    from crdppf.models import RoadNoise, ForestLimits, ForestDistances
    Par
    $ from crdppf.models import RoadNoise, ForestLimits

    Suppression de la ligne
    $ 'r159_dist_foret': ForestDistances , ForestDistances
    Ne pas oublier d’enlever la , sur la ligne précédente

# Upgrade existing project

To upgrade an existing version of the project go into the root folder of your project
Make sure your on the master branch or the branch you want to be on:

to get the list of your local branches:
    $ git branch

change on master if needed:   
 
    $ git checkout master

or create a new branch of your choice if you don't want to overwrite the master:

    $ git checkout -b [mynewbranch]
    
Fetch the global application part:

    $ git fetch upstream
    $ git merge upstream/master
 
if you are updating the inital install to the generalized version you probably get a message 'could not remove crdppf/.../ext' or so. Just delete the folder by

    $ rm -r crdppf

Get the submodule crdppf_core (https://github.com/SIT-Jura/crdppf_core.git if you'd like to get the core project too)

    $ git submodule update --init
    
Once it is installed get all the libraries of the submodule (ext, openlayers, ...)

     $ cd crdppf_core
     $ git submodule update --init
     
Now you should be up to date and ready to (re)build the application. Don't forget to include the project in the Apache configuration and to restart.