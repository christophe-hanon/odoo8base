.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

Intrastat reports for Belgium
=============================

This module implements the Belgian Intrastat reporting.

The report can be reviewed and corrected where needed before
the creation of the XML file for the online declaration (ONEGATE).

More information can be found on the National Bank website:
https://www.nbb.be/en/statistics/foreign-trade

Configuration
=============

This module adds the following configuration parameters:

* Company

  - Arrivals : Exempt, Standard or Extended
  - Dispatches : Exempt, Standard or Extended
  - Default Intrastat Region
  - Default Intrastat Transport Mode (Extended Declaration)
  - Default Intrastat Incoterm (Extended Declaration)

* Warehouse
  - Intrastat Region to cope with warehouses in different regions

* Inrastat Codes, Supplementary Units, Transaction Tyoes, Transport Modes, Regions

  Cf. menu Accounting / Configuration / Miscellaneous / Intrastat Configuration

  The configuration data is loaded when installing the module.

  A configuration wizard also allows to update the Intrastat Codes so that you can easily
  synchronise your Odoo instance with the latest list of codes supplied with this module
  (an update is published on an annual basis by the Belgian National Bank).

  Some Intrastat Codes require an Intrastat Supplementary Unit.
  In this case, an extra configuration is needed to map the Intrastat Supplementary Unit
  to the corresponding Odoo Unit Of Measurement.

* Product

  You can define a default Intrastat Code on the Product or the Product Category.

Known issues / Roadmap
======================

- This module is NOT compatible with the 'report_intrastat' and
  'l10n_be_intrastat' modules distributed via the Odoo standard addons.

- Product movements without invoices are not included in the current version
  of this module and must be added manually to the report lines
  before generating the ONEGATE XML declaration.

Credits
=======

Authors
-------
* Luc De Meyer, Noviat <info@noviat.com>

Maintainer
----------
.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
