import ComponentTypes from '@theme-original/NavbarItem/ComponentTypes';
import NestedDropdownNavbarItem from '@site/src/components/NestedDropdownNavbarItem';

// Register the custom navbar item type used for nested (sub-sub) dropdown
// fold-outs, e.g. the Toolbar scripts hierarchy and the Resolve/Fusion topic
// tree.
export default {
  ...ComponentTypes,
  'custom-nestedDropdown': NestedDropdownNavbarItem,
};
