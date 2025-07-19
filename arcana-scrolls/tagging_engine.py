import re
from typing import List, Dict, Any

def gpt_generate_tags(text) -> List[Dict[str, Any]]:
    """
    Calls GPT to extract semantic tags using theme, relationship, and emotion schemas.
    Tag format: {type: 'relationship/theme/emotion', tag: 'gabby#emotional_friction', description: 'Tension this morning', parent: 'gabby'}
    """
    # For now, return stubbed tags for testing
    # In production, call OpenAI API here
    return [
        {"type": "relationship", "tag": "gabby#emotional_friction", "description": "Tension this morning", "parent": "gabby"},
        {"type": "theme", "tag": "focus#routine", "description": "Morning focus on routine", "parent": "focus"},
        {"type": "emotion", "tag": "emotion#anxiety", "description": "Felt anxious", "parent": "emotion"}
    ]

class TagNode:
    def __init__(self, tag: str, tag_type: str, description: str = "", parent: str = None):
        self.tag = tag
        self.type = tag_type
        self.description = description
        self.parent = parent
        self.children = []
    def add_child(self, child):
        self.children.append(child)
    def to_dict(self):
        return {
            "tag": self.tag,
            "type": self.type,
            "description": self.description,
            "parent": self.parent,
            "children": [c.to_dict() for c in self.children]
        }

def build_tag_tree(tags: List[Dict[str, Any]]) -> List[TagNode]:
    """
    Build a tag tree from a flat list of tag dicts.
    """
    nodes = {t['tag']: TagNode(t['tag'], t['type'], t.get('description', ''), t.get('parent')) for t in tags}
    roots = []
    for t in tags:
        node = nodes[t['tag']]
        parent_tag = t.get('parent')
        if parent_tag and parent_tag in nodes:
            nodes[parent_tag].add_child(node)
        else:
            roots.append(node)
    return roots

def flatten_tag_tree(tree: List[TagNode], prefix: str = "") -> List[str]:
    """
    Flatten a tag tree for UI selection (e.g., 'gabby > emotional_friction').
    """
    result = []
    for node in tree:
        label = f"{prefix}{node.tag.split('#')[-1]}"
        result.append(label)
        if node.children:
            result.extend(flatten_tag_tree(node.children, prefix=label + " > "))
    return result

