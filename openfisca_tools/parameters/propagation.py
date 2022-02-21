from openfisca_core.parameters import Parameter, ParameterNode


def propagate_parameter_metadata(root: ParameterNode) -> ParameterNode:
    """Passes parameter metadata to descendents where this is specified.

    Args:
        root (ParameterNode): The root node.

    Returns:
        ParameterNode: The edited parameter root.
    """

    for parameter in root.get_descendants():
        if parameter.metadata.get("propagate_metadata_to_children"):
            for descendant in parameter.get_descendants():
                descendant.metadata.update(parameter.metadata)

    return root
