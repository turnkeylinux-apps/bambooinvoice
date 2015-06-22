BambooInvoice - Simple, Beautiful Online Invoicing
==================================================

`BambooInvoice`_ is invoicing software intended for small businesses and
independent contractors. It prioritizes ease of use, a clean
user-interface, and beautiful code. It was created by designer and
programmer Derek Allard, who uses it every day. It is meant to be sexy,
both on top of, and under the hood.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- BambooInvoice configurations:
   
   - Installed from upstream source code to /var/www/bambooinvoice

- SSL support out of the box
- `Adminer`_ administration frontend for MySQL (listening on port
  12322 - uses SSL).
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2, PHP, MySQL and Postfix.

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, phpMyAdmin: username **root**
-  BambooInvoice: default username is email set at first boot.


.. _BambooInvoice: http://bambooinvoice.org/
.. _TurnKey Core: http://www.turnkeylinux.org/core
.. _Adminer: http://www.adminer.org/
