from setuptools import find_packages, find_namespace_packages, setup, Extension
from Cython.Build import cythonize
import numpy
import os
import urllib.request
import zipfile
import tarfile
import platform

VERSION = '2.0.6'

RAYLIB_BASE = 'https://github.com/raysan5/raylib/releases/download/5.0/'

RAYLIB_NAME = 'raylib-5.0_macos' if platform.system() == "Darwin" else 'raylib-5.0_linux_amd64'

RAYLIB_LINUX = 'raylib-5.0_linux_amd64'
RAYLIB_LINUX_URL = RAYLIB_BASE + RAYLIB_LINUX + '.tar.gz'
if not os.path.exists(RAYLIB_LINUX):
    urllib.request.urlretrieve(RAYLIB_LINUX_URL, RAYLIB_LINUX + '.tar.gz')
    with tarfile.open(RAYLIB_LINUX + '.tar.gz', 'r') as tar_ref:
        tar_ref.extractall()

    os.remove(RAYLIB_LINUX + '.tar.gz')

RAYLIB_MACOS = 'raylib-5.0_macos'
RAYLIB_MACOS_URL = RAYLIB_BASE + RAYLIB_MACOS + '.tar.gz'
if not os.path.exists(RAYLIB_MACOS):
    urllib.request.urlretrieve(RAYLIB_MACOS_URL, RAYLIB_MACOS + '.tar.gz')
    with tarfile.open(RAYLIB_MACOS + '.tar.gz', 'r') as tar_ref:
        tar_ref.extractall()

    os.remove(RAYLIB_MACOS + '.tar.gz')

RAYLIB_WASM = 'raylib-5.0_webassembly'
RAYLIB_WASM_URL = RAYLIB_BASE + RAYLIB_WASM + '.zip'
if not os.path.exists(RAYLIB_WASM):
    urllib.request.urlretrieve(RAYLIB_WASM_URL, RAYLIB_WASM + '.zip')
    with zipfile.ZipFile(RAYLIB_WASM + '.zip', 'r') as zip_ref:
        zip_ref.extractall()

    os.remove(RAYLIB_WASM + '.zip')

extension_paths = [
    'pong/cy_pong',
]

system = platform.system()
if system == 'Darwin':
    # On macOS, use @loader_path.
    # The extension “.so” is typically in pufferlib/ocean/...,
    # and “raylib/lib” is (maybe) two directories up from ocean/<env>.
    # So @loader_path/../../raylib/lib is common.
    RAYLIB_INCLUDE = f'{RAYLIB_MACOS}/include'
    RAYLIB_LIB = f'{RAYLIB_MACOS}/lib'
elif system == 'Linux':
    # TODO: Check if anything moves packages around after they are installed.
    # That would break this linking. Rel path doesn't work outside the pufferlib dir
    RAYLIB_INCLUDE = f'{RAYLIB_LINUX}/include'
    RAYLIB_LIB = f'{RAYLIB_LINUX}/lib'
else:
    raise ValueError(f'Unsupported system: {system}')

extensions = [Extension(
    path.replace('/', '.'),
    [path + '.pyx'],
    include_dirs=[numpy.get_include(), RAYLIB_INCLUDE],
    extra_compile_args=['-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION', '-DPLATFORM_DESKTOP', '-O2', '-Wno-alloc-size-larger-than', '-fwrapv'],#, '-g'],
    extra_link_args=['-Bsymbolic-functions', '-O2', '-fwrapv'],
    extra_objects=[f'{RAYLIB_LIB}/libraylib.a']
) for path in extension_paths]

# Prevent Conda from injecting garbage compile flags
from distutils.sysconfig import get_config_vars
cfg_vars = get_config_vars()
for key in ('CC', 'CXX', 'LDSHARED'):
    if cfg_vars[key]:
        cfg_vars[key] = cfg_vars[key].replace('-B /root/anaconda3/compiler_compat', '')
        cfg_vars[key] = cfg_vars[key].replace('-pthread', '')
        cfg_vars[key] = cfg_vars[key].replace('-fno-strict-overflow', '')

for key, value in cfg_vars.items():
    if value and '-fno-strict-overflow' in str(value):
        cfg_vars[key] = value.replace('-fno-strict-overflow', '')


# setup(
#     ext_modules=cythonize("c_gae.pyx"),
#     include_dirs=[numpy.get_include()],
# )


setup(
    name="pufferlib",
    description="PufferAI Library"
    "PufferAI's library of RL tools and utilities",
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=find_namespace_packages() + find_packages(),
    package_data={
        "pufferlib": [
            f'{RAYLIB_LIB}/libraylib.a',
        ]
    },
    include_package_data=True,
    ext_modules = cythonize([
        "pufferlib/extensions.pyx",
        "c_gae.pyx",
        "pufferlib/puffernet.pyx",
        *extensions,
    ], 
    ),
    include_dirs=[numpy.get_include(), RAYLIB_INCLUDE],
)