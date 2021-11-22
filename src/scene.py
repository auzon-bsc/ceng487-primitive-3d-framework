class Scene:
    """
    Scene class holds 3D objects.

    """
    _objectList: list

    def __init__(self) -> None:
        """
        Initialize empty Scene object
        """
        self._objectList = []

    def addObj3D(self, obj3D):
        """
        Add a 3D object

        Args:
            obj3D (Obj3d): 3D object to add
        """
        self._objectList.append(obj3D)

    def removeObj3D(self, obj3D):
        """
        Remove a 3D object

        Args:
            obj3D (Obj3d): 3D object to remove

        Returns:
            Obj3d: Removed object
        """
        removedObj3D = self._objectList.remove(obj3D)
        return removedObj3D

    def popObj3D(self, index):
        """
        Pop a 3D object according to given index

        Args:
            index (int): Index of the 3D object that wanted to be popped

        Returns:
            Obj3d: Popped 3D object
        """
        poppedObj3D = self._objectList.pop(index)
        return poppedObj3D

    def getObj3D(self, index):
        """
        Get 3D object where the given index points

        Args:
            index (int): Index of the wanted 3D object

        Returns:
            Obj3d: 3D object at the given index
        """
        wantedObj3D = self._objectList[index]
        return wantedObj3D
