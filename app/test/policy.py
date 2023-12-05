from . import tests as _tests

class TestPolicy(object):
    """ Password policy that contains a list of tests."""
    
    @classmethod
    def all_tests(cls):
        """ Get a dict of available tests

            :returns: { test-name: TestClass }
            :rtype: dict[type]
        """
        return dict(_tests.BaseTest.test_classes)

    @classmethod
    def from_names(cls, **tests):
        """ Init password policy from a dictionary of test definitions.

        A test definition is simply:

            { test-name: argument } or { test-name: [arguments] }

        Test name is just a lowercased class name.

        Example:

            PasswordPolicy.from_names(
                length=8,
                strength=(0.33, 30),
            )

        :param tests: Dict of test definitions.
        :rtype: PasswordPolicy
        :raises KeyError: wrong test name
        """
        _tests.ATest.test_classes['length'](8)
        tests = [ _tests.ATest.test_classes[name](
                      *(args if isinstance(args, (list, tuple)) else [args])
                  ) for name, args in tests.items() ]
        return cls(*tests)
 
    
    def __init__(self, *tests):
        self._tests = tests
        
    

    def run(self):
        return self.run()