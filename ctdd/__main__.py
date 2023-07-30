
import sys, os, subprocess, re
from dataclasses import dataclass

@dataclass
class _ContentSet:
    h: str = ''
    c: str = ''
    py: str = ''

    def get(self, key):
        if 'h' == key:
            return self.h

        if 'c' == key:
            return self.c

        if 'py' == key:
            return self.py

        raise ValueError(f'invalid key "{key}"')


_file_content_set = _ContentSet(
    h=r"""#pragma once

{content}
""", c=r"""#include "{full_name}.h"

{content}
""", py=r"""from ctdd import Tester

class BootstrapTests(Tester):
    def test_sut_compiles(self):
        self.assertIsNotNone(self.sut)

{content}

Tester.go()
""")

_test_content_set = _ContentSet(py=r"""
class {Name}Tests(Tester):
    pass
""")

_class_content_set = _ContentSet(h=r"""
struct {name}_config_t
{{
    char const *name;
}};

struct {name}_state_t
{{
    struct {name}_config_t config;
}};

int {name}_init(struct {name}_state_t *, struct {name}_config_t const *);
void {name}_run(struct {name}_state_t *);
""", c=r"""
int {name}_init(struct {name}_state_t *state, struct {name}_config_t const *config)
{{
    state->config = *config;

    return -1;
}}

void {name}_run(struct {name}_state_t *state)
{{
}}
""", py=r"""
class InitTests(Tester):
    def test_init_copies_config(self):
        expected = "{name}"

        config = self.factory.{name}_config_t()
        config.name = self.factory.C_string(expected)
        state = self.factory.{name}_state_t()
        
        self.sut.{name}_init(state, config)
        actual = self.factory.P_str(config.name)

        self.assertEqual(expected, actual)
        
        
    def test_init_returns_zero(self):
        config = self.factory.{name}_config_t()
        state = self.factory.{name}_state_t()
        
        self.assertEqual(0, self.sut.{name}_init(state, config))
""")


def _emit_files(name, exts, file_templates, content_templates):
    clean_name = _clean_name(name)

    replacements = {
        'full_name': name,
        'Name': clean_name.title(),
        'name': clean_name.lower()
    }
    for ext in exts:
        content = content_templates.get(ext).format_map(replacements)
        replacements['content'] = content
        file = file_templates.get(ext).format_map(replacements)

        filename = f'{name}.{ext}'

        print(f'creating {filename}')

        with open(filename, 'w') as f:
            f.write(file)


def _clean_name(name):
    if name.endswith('_tests'):
        name = name[:-6]

    if name.endswith('_test'):
        name = name[:-5]

    return name


def _discover(root_path:str) -> int:
    # print(f'discovering tests rooted at {root_path}')

    tree = [{'path':x[0], 'folders':x[1], 'files':x[2]} for x in os.walk(root_path)]

    errors = []
    fails = []
    warnings = []
    total_output = ''
    total_results = ''
    
    total_number_of_tests = 0
    total_number_of_errors = 0
    total_number_of_fails = 0
    total_number_of_warnings = 0

    for node in tree:
        files = node['files']

        py_files = [(x[:-3], node['path'],) for x in files if x.endswith('.py')] or None
        c_files = [x[:-2] for x in files if x.endswith('.c')]
        h_files = [x[:-2] for x in files if x.endswith('.h')]

        if py_files:
            ctdd_tests = [x for x in py_files if x[0] in c_files and x[0] in h_files] or None

            if ctdd_tests:
                for test in ctdd_tests:
                    py_filename = f'{test[1]}/{test[0]}.py'

                    process = subprocess.Popen(['python3', py_filename],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()

                    test_output = stdout.decode()
                    test_results = stderr.decode()

                    number_of_errors = 0
                    number_of_fails = 0
                    number_of_warnings = 0

                    x = re.search('^Ran (\d+) test', test_results, re.MULTILINE)
                    if x:
                        number_of_tests = int(x.group(1) or 0)

                        for line in test_results.split('\n'):
                            if line.startswith('ERROR: '):
                                errors.append(line)
                                number_of_errors += 1

                            if line.startswith('FAIL: '):
                                fails.append(line)
                                number_of_fails += 1

                            if 'warning: ' in line:
                                warnings.append(line)
                                number_of_warnings += 1

                        print(f'{test[0]}: tests: {number_of_tests}, errors: {number_of_errors}, fails: {number_of_fails}, warnings: {number_of_warnings}')

                        total_number_of_tests += number_of_tests
                        total_number_of_fails += number_of_fails
                        total_number_of_errors += number_of_errors
                        total_number_of_warnings += number_of_warnings
                    else:
                        print(f'{test[0]}: build failed')

                        total_number_of_errors += 1
     
                    total_output += test_output
                    total_results += test_results


    with open('ctdd_output.log', 'w') as f:
        f.write(total_output)

    with open('ctdd_results.log', 'w') as f:
        f.write(total_results)

    if errors:
        print(errors)

    if fails:
        print(fails)

    print(f'total tests: {total_number_of_tests}, errors: {total_number_of_errors}, fails: {total_number_of_fails}, warnings: {total_number_of_warnings}')

    return 0 if 0 == total_number_of_errors and 0 == total_number_of_fails else 1

def main() -> int:

    if '-c' == sys.argv[1]:
        name = sys.argv[2]
        print(f'creating class "{name}" tester files')
        _emit_files(name, ('h', 'c', 'py'),
                    _file_content_set, _class_content_set)

    if '-t' == sys.argv[1]:
        name = sys.argv[2]
        print(f'creating test "{name}" tester file')
        _emit_files(name, ('h', 'c', 'py',),
                    _file_content_set, _test_content_set)

    if '-d' == sys.argv[1]:
        path = os.path.abspath(os.path.expanduser(sys.argv[2]))
        sys.exit(_discover(root_path=path))

if __name__ == '__main__':
    sys.exit(main())
