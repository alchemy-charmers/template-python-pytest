from ${libfile} import ${libclass}
from charmhelpers.core import hookenv
from charms.reactive import set_flag, when, when_not

helper = ${libclass}()

@when_not('${metadata.package}.installed')
def install_${metadata.package.replace('-', '_')}():
    #raw
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    #end raw
    hookenv.status_set('active','')
    set_flag('${metadata.package}.installed')
