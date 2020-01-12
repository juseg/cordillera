Cordilleran ice sheet glacial cycle simulations continuous variables
--------------------------------------------------------------------

Files [required]::

   ciscyc4.10km.epica.0590.ex.1ka.nc
   ciscyc4.10km.epica.0590.ts.10a.nc
   ciscyc4.10km.grip.0620.ex.1ka.nc
   ciscyc4.10km.grip.0620.ts.10a.nc
   ciscyc4.10km.ngrip.0660.ex.1ka.nc
   ciscyc4.10km.ngrip.0660.ts.10a.nc
   ciscyc4.10km.odp1012.0615.ex.1ka.nc
   ciscyc4.10km.odp1012.0615.ts.10a.nc
   ciscyc4.10km.odp1020.0605.ex.1ka.nc
   ciscyc4.10km.odp1020.0605.ts.10a.nc
   ciscyc4.10km.vostok.0595.ex.1ka.nc
   ciscyc4.10km.vostok.0595.ts.10a.nc
   ciscyc4.5km.epica.0590.ex.1ka.nc
   ciscyc4.5km.epica.0590.ts.10a.nc
   ciscyc4.5km.grip.0620.ex.1ka.nc
   ciscyc4.5km.grip.0620.ts.10a.nc

Communities [recommended]
   --

Upload type [required]
   Dataset

Basic information [required]
   Digital Object Identifier
      -

   Publication date
      -

   Title
      Cordilleran ice sheet glacial cycle simulations continuous variables

   Authors
      Seguinot, Julien

   Description
      These data contain a subset of time-dependent glacier model output
      variables:

      **Reference**:

      * J. Seguinot, I. Rogozhina, A. P. Stroeven, M. Margold, and J. Kleman.
        Numerical simulations of the Cordilleran ice sheet through the last
        glacial cycle,
        *The Cryosphere*, 10(2):639–664,
        https://doi.org/10.5194/tc-10-639-2016, 2016.

      **File names**::

         ciscyc4.{10km|5km}.{forcing}.{ex.1ka|ts.10a}.nc

      * Horizontal resolution:

        - *10km*: 10 km horizontal resolution
        - *5km*: 5 km horizontal resolution

      * Temperature forcing:

        - *epica*: EPICA ice core temperature forcing
        - *grip*: GRIP ice core temperature forcing
        - *ngrip*: NGRIP ice core temperature forcing
        - *odp1012*: ODP 1012 ocean core temperature forcing
        - *odp1020*: ODP 1020 ocean core temperature forcing
        - *vostok*: Vostok ice core temperature forcing

      * Variable types:

        - *ex.1ka*: spatial diagnostics every thousand years
        - *ts.10a*: scalar time-series every ten years

      **Data format**

      The data use compressed netCDF format. For quick inspection I recommend
      ncview. Spatial diagnostics (*\*.ex.1ka.nc*) can be converted to
      GeoTIFF (and other GIS formats) e.g. using GDAL::

         gdal_translate NETCDF:filename.nc:variable -b band filename.variable.band.tif

      The list of variables (subdatasets) can be obtained from ncdump or
      gdalinfo. The *band* number equals 120 minus the age in ka. Band
      information can be displayed with::

         gdalinfo NETCDF:filename.nc:variable

      Variable long names, units, PISM configuration parametres and additional
      information are contained within the netCDF metadata.


   Version
      --

   Language
      en

   Keywords
      cordillera, glacier, ice sheet, modelling

   Additional notes
      This work was supported by the Swedish Research Council (VR) grant
      2008-3449, the German Academic Exchange Service (DAAD) grant 50015537,
      the Knut and Alice Wallenberg Foundation, the Swedish National
      Infrastructure for Computing (SNIC) grants 2013/1-159 and 2014/1-159, and
      the Swiss National Supercomputing Centre (CSCS) grant s573.

License [required]
   Open Access / Creative Commons Attribution 4.0

Funding [recommended]
   -- (not working)

Related/alternate identifiers [recommended]
   https://doi.org/10.5194/tc-10-639-2016 is supplemented by this upload
   https://doi.org/10.5281/zenodo.1423160 is referenced by this upload

Contributors [optional]
   Rogozhina, Irina
   Stroeven, Arjen P.
   Margold, Martin
   Kleman, Johan

References [optional]

   * Amante, C. and Eakins, B. W.: ETOPO1 1 arc-minute global relief model:
     procedures, data sources and analysis, NOAA technical memorandum NESDIS
     NGDC-24, Natl. Geophys. Data Center, NOAA, Boulder, CO,
     https://doi.org/10.7289/V5C8276M, 2009.

   * Andersen, K. K., Azuma, N., Barnola, J.-M., Bigler, M., Biscaye, P.,
     Caillon, N., Chappellaz, J., Clausen, H. B., Dahl-Jensen, D., Fischer, H.,
     Fl\"uckiger, J., Fritzsche, D., Fujii, Y., Goto-Azuma, K., Grønvold,
     K., Gundestrup, N. S., Hansson, M., Huber, C., Hvidberg, C. S., Johnsen,
     S. J., Jonsell, U., Jouzel, J., Kipfstuhl, S., Landais, A., Leuenberger,
     M., Lorrain, R., Masson-Delmotte, V., Miller, H., Motoyama, H., Narita,
     H., Popp, T., Rasmussen, S. O., Raynaud, D., Rothlisberger, R., Ruth, U.,
     Samyn, D., Schwander, J., Shoji, H., Siggard-Andersen, M.-L., Steffensen,
     J. P., Stocker, T., Sveinbjörnsdóttir, A. E., Svensson, A., Takata, M.,
     Tison, J.-L., Thorsteinsson, T., Watanabe, O., Wilhelms, F., and White, J.
     W. C.: High-resolution record of Northern Hemisphere climate extending
     into the last interglacial period, Nature, 431, 147–151,
     https://doi.org/10.1038/nature02805, data archived at the World Data
     Center for Paleoclimatology, Boulder, Colorado, USA, 2004.

   * Dansgaard, W., Johnsen, S. J., Clausen, H. B., Dahl-Jensen, D.,
     Gundestrup, N. S., Hammer, C. U., Hvidberg, C. S., Steffensen, J. P.,
     Sveinbjörnsdottir, A. E., Jouzel, J., and Bond, G.: Evidence for general
     instability of past climate from a 250-kyr ice-core record, Nature, 364,
     218–220, https://doi.org/10.1038/364218a0, data archived at the World Data
     Center for Paleoclimatology, Boulder, Colorado, USA., 1993.

   * Herbert, T. D., Schuffert, J. D., Andreasen, D., Heusser, L., Lyle, M.,
     Mix, A., Ravelo, A. C., Stott, L. D., and Herguera, J. C.: Collapse of the
     California current during glacial maxima linked to climate change on land,
     Sience, 293, 71–76, https://doi.org/10.1126/science.1059209, data
     archived at the World Data Center for Paleoclimatology, Boulder, Colorado,
     USA, 2001.

   * Jouzel, J., Masson-Delmotte, V., Cattani, O., Dreyfus, G., Falourd, S.,
     Hoffmann, G., Minster, B., Nouet, J., Barnola, J. M., Chappellaz, J.,
     Fischer, H., Gallet, J. C., Johnsen, S., Leuenberger, M., Loulergue, L.,
     Luethi, D., Oerter, H., Parrenin, F., Raisbeck, G., Raynaud, D., Schilt,
     A., Schwander, J., Selmo, E., Souchez, R., Spahni, R., Stauffer, B.,
     Steffensen, J. P., Stenni, B., Stocker, T. F., Tison, J. L., Werner, M.,
     and Wolff, E. W.: Orbital and Millennial Antarctic Climate Variability
     over the Past 800,000 Years, Sience, 317, 793–796,
     https://doi.org/10.1126/science.1141038, data archived at the World Data
     Center for Paleoclimatology, Boulder, Colorado, USA., 2007.

   * Mesinger, F., DiMego, G., Kalnay, E., Mitchell, K., Shafran, P. C.,
     Ebisuzaki, W., Jović, D., Woollen, J., Rogers, E., Berbery, E. H., Ek, M.
     B., Fan, Y., Grumbine, R., Higgins, W., Li, H., Lin, Y., Manikin, G.,
     Parrish, D., and Shi, W.: North American regional reanalysis, B. Am.
     Meteorol. Soc., 87, 343–360, https://doi.org/10.1175/BAMS-87-3-343, 2006.

   * Petit, J. R., Jouzel, J., Raynaud, D., Barkov, N. I., Barnola, J.-M.,
     Basile, I., Bender, M., Chappellaz, J., Davis, M., Delaygue, G., Delmotte,
     M., Kotlyakov, V. M., Legrand, M., Lipenkov, V. Y., Lorius, C., Pépin, L.,
     Ritz, C., Saltzman, E., and Stievenard, M.: Climate and atmospheric
     history of the past 420,000 years from the Vostok ice core, Antarctica,
     Nature, 399, 429–436, https://doi.org/10.1038/20859, data archived at the
     World Data Center for Paleoclimatology, Boulder, Colorado, USA., 1999.

   * the PISM authors: PISM, a Parallel Ice Sheet Model,
     http://www.pism-docs.org, 2015.

   * Winkelmann, R., Martin, M. A., Haseloff, M., Albrecht, T., Bueler, E.,
     Khroulev, C., and Levermann, A.: The Potsdam Parallel Ice Sheet Model
     (PISM-PIK) – Part 1: model description, The Cryosphere, 5, 715–726,
     https://doi.org/10.5194/tc-5-715-2011, 2011.

Journal [optional]
   --

Conference [optional]
   --

Book/Report/Chapter [optional]
   --

Thesis [optional]
   --

Subjects [optional]
   --
