from setuptools import find_packages, setup

package_name = 'vo_local_planner'

setup(
    name=package_name,
    version='0.0.0',
    packages=['vo_local_planner'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kjs0209',
    maintainer_email='rkdwnstj020209@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
             'vo_planner_test = vo_local_planner.vo_planner_test:main',
             'controller_test_node = vo_local_planner.controller_test_node:main',
             'vo_planner_test2 = vo_local_planner.vo_planner_test2:main',
             'vo_planner = vo_local_planner.vo_planner:main',
        ],
    },
)
