import argparse
import subprocess
from pkg_resources import get_distribution, DistributionNotFound

def get_dependencies(package_name, max_depth, current_depth=0, seen=None):
    if seen is None:
        seen = set()
    if current_depth > max_depth:
        return []
    try:
        distribution = get_distribution(package_name)
    except DistributionNotFound:
        return []

    dependencies = []
    for requirement in distribution.requires():
        if requirement.key not in seen:
            seen.add(requirement.key)
            dependencies.append(requirement.key)
            dependencies.extend(get_dependencies(requirement.key, max_depth, current_depth + 1, seen))
    return dependencies

def generate_plantuml(package_name, dependencies):
    uml = "@startuml\n"
    uml += f'package "{package_name}" {{\n'
    for dep in dependencies:
        uml += f'  "{package_name}" --> "{dep}"\n'
    uml += "}\n@enduml"
    return uml

def main():
    parser = argparse.ArgumentParser(description='Visualize Python package dependencies.')
    parser.add_argument('visualizer_path', help='Path to the graph visualization program')
    parser.add_argument('package_name', help='Name of the package to analyze')
    parser.add_argument('max_depth', type=int, help='Maximum depth of dependency analysis')
    parser.add_argument('repository_url', help='URL of the repository')

    args = parser.parse_args()

    dependencies = get_dependencies(args.package_name, args.max_depth)
    plantuml_code = generate_plantuml(args.package_name, dependencies)

    with open('dependencies.uml', 'w') as f:
        f.write(plantuml_code)

    subprocess.run(["java", "-jar", args.visualizer_path, 'dependencies.uml'])

if __name__ == '__main__':
    main()