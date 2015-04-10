CRDPPF Portal
============

# Getting started

  
Checkout the source code with a ssh key (see https://help.github.com/articles/generating-ssh-keys):

    $ git clone git@github.com:SIT-Jura/crdppf.git

or when you're not using ssh key:

    $ git clone https://github.com/SIT-Jura/crdppf.git

Get the submodule crdppf_core (https://github.com/sitn/crdppf_core.git if you'd like to get the core project too)

    $ cd crdppf
    $ git submodule update --init
    
Once it is installed get all the libraries of the submodule (ext, openlayers, ...)

    $ cd crdppf_core
    $ git submodule update --init
     
maybe a 

    $ git submodule foreach git submodule update --init

Bootstrap and buildout

    $ cd ..
    $ python bootstrap.py --version 1.5.2 --distribute --download-base \
        http://pypi.camptocamp.net/distribute-0.6.22_fix-issue-227/ --setup-source \
        http://pypi.camptocamp.net/distribute-0.6.22_fix-issue-227/distribute_setup.py

After the installation put the directoriy crdpp in W

    $ cd ..
    $ chmod -R o+w crdppf

# Create your own buildout file by:
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

or
    $ ./refresh xxxx

Or, copy-paste and adapt `buildout_rwunderlich.cfg`
Change 

    $ instanceid = xxxx
    
This variable can't the same as another instance existance

# Change in crdppf_core (not in variable)
Changement a effectuer dans crdppf_core en attendant que cela passe en variable dans le projet NE
Plus de modifications depuis la version 1.1.0         

crdppf/crdppf_core/crdppf/util/pdf_classes.py
Changer la ligne 512

    $ <sld:CssParameter name="font-family">arial</sld:CssParameter>

# Upgrade and update crdppf_core

To upgrade crdppf_core version of the project go into the crdppf_core folder of your project
Make sure your on the master branch or the branch you want to be on:

to get the list of your local branches:
    $ git branch

change on master if needed:   
 
    $ git checkout master

or create a new branch of your choice if you don't want to overwrite the master:

    $ git checkout -b [mynewbranch]
    
Update and upgrade:

    $ cd crdppf_core
    $ git fetch
    $ git checkout <tag>
    $ git submodule sync
    $ git submodule update --init

<tag> is the version of crdppf_core (ex: 1.0.7) 
     
Now you should be up to date and ready to (re)build the application. Don't forget to include the project in the Apache configuration and to restart.