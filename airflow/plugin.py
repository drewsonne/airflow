class AirflowConfigurationProviderPlugin(object):
    """
    Providers an interface for retrieving configurations
    from an arbitrary source
    """

    priority = 0

    def get_var_option(self, section, key):
        """
        For a given section and key, return  a configuration result
        if this provider has this section and key available.

        :param section: Section of the airflow config to search for the key in
        :type section: basestring
        :param key: Unique identifier within the section to search for a configuration value in
        :type key: basestring
        """
        raise NotImplementedError

    def has_section(self, section):
        """
        Return true if the provider has the section in question

        :param section: section from the config
        :return:
        """
        raise NotImplementedError

    def get_section(self, section):
        """
        Returns the section as a dict. Values are converted to int, float, bool
        as required.
        :param section: section from the config
        :return: dict
        """
        raise NotImplementedError
