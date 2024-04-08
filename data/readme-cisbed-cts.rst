Cordilleran ice sheet improved bedrock simulations continuous variables
-----------------------------------------------------------------------

Files [required]::

   cisbed.10km.epica.dav13.ex.100a.nc
   cisbed.10km.epica.dav13.ts.10a.nc
   cisbed.10km.epica.ghf70.ex.100a.nc
   cisbed.10km.epica.ghf70.ts.10a.nc
   cisbed.10km.epica.gou11comb.ex.100a.nc
   cisbed.10km.epica.gou11comb.ts.10a.nc
   cisbed.10km.epica.gou11simi.eet30km.ex.100a.nc
   cisbed.10km.epica.gou11simi.eet30km.ts.10a.nc
   cisbed.10km.epica.gou11simi.ex.100a.nc
   cisbed.10km.epica.gou11simi.num1e21.ex.100a.nc
   cisbed.10km.epica.gou11simi.num1e21.ts.10a.nc
   cisbed.10km.epica.gou11simi.ts.10a.nc
   cisbed.10km.epica.sha04.ex.100a.nc
   cisbed.10km.epica.sha04.ts.10a.nc
   cisbed.10km.grip.dav13.ex.100a.nc
   cisbed.10km.grip.dav13.ts.10a.nc
   cisbed.10km.grip.ghf70.ex.100a.nc
   cisbed.10km.grip.ghf70.ts.10a.nc
   cisbed.10km.grip.gou11comb.ex.100a.nc
   cisbed.10km.grip.gou11comb.ts.10a.nc
   cisbed.10km.grip.gou11simi.eet30km.ex.100a.nc
   cisbed.10km.grip.gou11simi.eet30km.ts.10a.nc
   cisbed.10km.grip.gou11simi.ex.100a.nc
   cisbed.10km.grip.gou11simi.num1e21.ex.100a.nc
   cisbed.10km.grip.gou11simi.num1e21.ts.10a.nc
   cisbed.10km.grip.gou11simi.ts.10a.nc
   cisbed.10km.grip.sha04.ex.100a.nc
   cisbed.10km.grip.sha04.ts.10a.nc
   cisbed.3km.epica.gou11simi.num1e21.ex.100a.nc
   cisbed.3km.epica.gou11simi.num1e21.ts.10a.nc
   cisbed.3km.grip.0620.gou11simi.num1e21.ex.100a.nc
   cisbed.3km.grip.0620.gou11simi.num1e21.ts.10a.nc
   cisbed.5km.epica.0590.ghf70.ex.100a.nc
   cisbed.5km.epica.0590.ghf70.ts.10a.nc
   cisbed.5km.grip.0620.ghf70.ex.100a.nc
   cisbed.5km.grip.0620.ghf70.ts.10a.nc

Communities [recommended]
   --

Basic information [required]
   Digital Object Identifier
      10.5281/zenodo.10940085

   Resource type [required]
      Dataset

   Title
      Cordilleran ice sheet improved bedrock simulations continuous variables

   Publication date
      -

   Creators
      Seguinot, Julien

   Description
      These data contain a subset of time-dependent glacier model output
      variables. The `ghf70` data files are an update on the reference below,
      fixing significant problems affecting the computation of the bedrock
      deformation in response to ice load (PISM Github issues
      [https://github.com/pism/pism/issues/370][#370] and
      [https://github.com/pism/pism/issues/377][#377]) and the computation of
      ice temperature (PISM Github issue
      [https://github.com/pism/pism/issues/371][#371]). The other data files
      additionally include spatially-variable geothermal heat flux (`dav13`,
      `gou11comb`, `gou11simi`, `sha04`), different lithospheric rigidity
      (`eet30km`) or mantle viscosity (`num1e21`), and higher horizontal
      resolution (`3km`).

      **Reference**:

      * Seguinot, J., Rogozhina, I., Stroeven, A. P.,  Margold, M. and
        Kleman, J.: Numerical simulations of the Cordilleran ice sheet through
        the last glacial cycle, The Cryosphere, 10(2), 639–664,
        https://doi.org/10.5194/tc-10-639-2016, 2016.

      **File names**::

         cisbed.{res}.{forcing}.{ex.100a|ex.1ka|ts.10a}.{ghf}.{props}.nc

      * Horizontal resolution:

        - *10km*: 10 km horizontal resolution
        - *5km*: 5 km horizontal resolution
        - *3km*: 3 km horizontal resolution

      * Temperature forcing:

        - *epica*: EPICA ice core temperature forcing
        - *grip*: GRIP ice core temperature forcing

      * Variable types:

        - *ex.100a*: spatial diagnostics every hundred years
        - *ts.10a*: scalar time-series every ten years

      * Geothermal heat flow:

        - *ghf70*: constant 70 mW m-2 heat flow
        - *dav13*: Davies (2013) geothermal heat flow map
        - *gou11comb*: Goutorbe et al. (2011) best combination method
        - *gou11simi*: Goutorbe et al. (2011) similarity method
        - *sha04*: Shapiro and Ritzwoller (2004) heat flow map

      * Bedrock properties

        - *eet30km*: lithosphere elastic thickness of 30 km
        - *num1e21*: astenosphere viscosity of 1e21 Pa s

      **Data format**:

      The data use compressed netCDF format. For quick inspection I recommend
      ncview. Spatial diagnostics (*\*.ex.\*.nc*) can be converted to
      GeoTIFF (and other GIS formats) e.g. using GDAL::

         gdal_translate NETCDF:filename.nc:variable -b band filename.variable.band.tif

      The list of variables (subdatasets) can be obtained from ncdump or
      gdalinfo. The *band* number equals 120 minus the age in ka. Band
      information can be displayed with::

         gdalinfo NETCDF:filename.nc:variable

      Variable long names, units, PISM configuration parametres and additional
      information are contained within the netCDF metadata.

      **Funding:**

      Swiss National Supercomputing Centre (CSCS) grants s573 and sm13 to
      J. Seguinot, Swiss National Science Foundation grants no.~200020-169558
      and 200021-153179/1 to M. Funk.

      **Changelog:**

      * Version 1:

         - Initial version.

   License
      Creative Commons Attribution 4.0 International

Recommended information
   Contributors
      --

   Keywords and subjects
      cordillera, glacier, ice sheet, modelling

   Languages
      en

   Dates
      --

   Version
      --

   Publisher
      Zenodo

Funding
   -- (not working)

Alternate identifiers
   --

Related works
   References 10.5194/tc-10-639-2016
   Is new version of 10.5281/zenodo.3606535

References [optional]

   * Davies, J. H.: Global map of solid Earth surface heat flow, Geochem.
     Geophys. Geosy., 14, 4608–4622, https://doi.org/10.1002/ggge.20271, 2013.

   * Goutorbe, B., Poort, J., Lucazeau, F., and Raillard, S.: Global heat flow
     trends resolved from multiple geological and geophysical proxies, Geophys.
     J. Int., 187, 1405–1419, https://doi.org/10.1111/j.1365-246x.2011.05228.x,
     2011.

   * Seguinot, J., Rogozhina, I., Stroeven, A. P.,  Margold, M. and Kleman, J.:
     Numerical simulations of the Cordilleran ice sheet through the last
     glacial cycle, The Cryosphere, 10(2), 639–664,
     https://doi.org/10.5194/tc-10-639-2016, 2016.

   * Shapiro, N. M. and Ritzwoller, M. H.: Inferring surface heat flux
     distributions guided by a global seismic model: particular application to
     Antarctica, Earth Planet. Sc. Lett., 223(1–2), 213-224,
     https://doi.org/10.1016/j.epsl.2004.04.011, 2004.

   * the PISM authors: PISM, a Parallel Ice Sheet Model,
     http://www.pism-docs.org, 2019.

Software
   Repository URL
      https://github.com/pism/pism/

   Programming language
      C++

   Development status
      Active

Publishing information
   --

Conference
   --

Domain specific fields
   --
