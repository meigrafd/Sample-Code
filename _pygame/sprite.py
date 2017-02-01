import pygame
from operator import truth
from functools import wraps


# Flag values for anchors.
# TODO: use Rect's constants
ANCHOR_TOPLEFT = 101
ANCHOR_TOPRIGHT = 102
ANCHOR_BOTTOMLEFT = 103
ANCHOR_BOTTOMRIGHT = 104
ANCHOR_CENTER = 105
ANCHOR_MIDTOP = 106
ANCHOR_MIDBOTTOM = 107
ANCHOR_MIDLEFT = 108
ANCHOR_MIDRIGHT = 109


def call_hook_method(hook_name):
    """decorator to wrap a method with a call to a hook method.

    The hook should return a boolean deciding whether to continue
    with the original method call."""
    def on_call(method):
        @wraps(method)
        def wrapped(self, *args, **kwargs):
            hook = getattr(self, hook_name, None)
            if hook:
                if hook(method, *args, **kwargs):
                    return method(self, *args, **kwargs)
        return wrapped
    return on_call


class Sprite(object):
    """simple base class for visible game objects

    pygame.sprite.Sprite(*groups): return Sprite

    The base class for visible game objects. Derived classes will want to
    override the Sprite.update() method and assign Sprite.image and Sprite.rect
    attributes.  The initializer can accept any number of Group instances that
    the Sprite will become a member of.

    When subclassing the Sprite class, be sure to call the base initializer
    before adding the Sprite to Groups.

    """

    def __init__(self, *groups):
        """initialize sprite instance

        Initializes attributes to default values, and optionally
        adds it to given groups.
        """
        self.image = self.original = None
        self.rect = None

        self.dirty = False

        # Initialize position
        self.anchor = ANCHOR_TOPLEFT
        self.position = None
        self.offset = (0, 0)
        self.layer = 0

        # Initialize visual attributes
        self.scale = 1
        self.rotate = 0
        self.visible = True

        self.__g = {}  # The groups the sprite is in
        if groups:
            self.add(*groups)

    def draw(self, surface):
        """draw the sprite's image on a surface

        Sprite.draw(surface): return Rect

        This should be called by a group's own `draw` method.

        On failure or if sprite should not be drawn, returns 0.
        """
        if (self.visible):
            return surface.blit(self.image, self.rect)
        else:
            return 0

    def on_visual_change(self, *args, **kwargs):
        """mark sprite as dirty on any visual change
        """
        self.dirty = True
        return True

    @call_hook_method('on_visual_change')
    def set_image(self, img):
        """set a new image object for the sprite
        """
        self.image = self.original = img
        self.update_image()

    def update_image(self):
        """update the sprite's image object

        usually useful for transformations, this method does
        not change the 'original' attribute."""
        img = self.original
        if img is not None:
            if self.scale != 1:
                img = pygame.transform.scale(img, self.scaled_size())
            if self.rotate != 0:
                img = pygame.transform.rotate(img, self.rotate)
            self.image = img
            self.rect = img.get_rect()
            self.move_to(self.position)

    def anchor_value(self):
        """return actual position of sprite's anchor

        If anchor was provided in coordinates, use them.
        Otherwise, translate anchor flags to coordinates.
        """
        #TODO handle negative values
        if type(self.anchor) is tuple:
            return self.anchor
        else:
            (w, h) = self.rect.size
            return {
                ANCHOR_TOPLEFT:     (0, 0),
                ANCHOR_TOPRIGHT:    (w, 0),
                ANCHOR_BOTTOMLEFT:  (0, h),
                ANCHOR_BOTTOMRIGHT: (w, h),
                ANCHOR_CENTER:      (w / 2, h / 2),
                ANCHOR_MIDTOP:      (w / 2, 0),
                ANCHOR_MIDBOTTOM:   (w / 2, h),
                ANCHOR_MIDLEFT:     (0, h / 2),
                ANCHOR_MIDRIGHT:    (w, h / 2)
            }[self.anchor]

    def update_position(self):
        """ re-calculating the sprite's rect position
        """
        (x, y) = self.position
        (off_x, off_y) = self.offset
        (anc_x, anc_y) = self.anchor_value()
        self.rect.topleft = (x + off_x - anc_x, y + off_y - anc_y)

    @call_hook_method('on_visual_change')
    def move_to(self, pos):
        """move sprite to a certain position
        """
        #TODO handle float values
        self.position = pos
        if pos:
            self.update_position()

    @call_hook_method('on_visual_change')
    def move_by(self, delta):
        """move sprite by a certain delta
        """
        (delta_x, delta_y) = delta
        (current_x, current_y) = self.position
        self.move_to((current_x + delta_x, current_y + delta_y))

    @call_hook_method('on_visual_change')
    def set_offset(self, offset):
        self.offset = offset
        self.update_position()

    @call_hook_method('on_visual_change')
    def make_visible(self):
        self.visible = True

    @call_hook_method('on_visual_change')
    def make_invisible(self):
        self.visible = False

    @call_hook_method('on_visual_change')
    def toggle_visibility(self):
        self.visible = not self.visible

    @call_hook_method('on_visual_change')
    def scale_to(self, ratio):
        """set sprite's scale ratio (overwriting)

        Ratio must be a positive float.
        """
        if ratio < 0:
            raise AttributeError("ratio must be a positive float")

        self.scale = ratio
        self.update_image()

    @call_hook_method('on_visual_change')
    def scale_by(self, ratio):
        """set sprite's scale ratio (accumalating)

        Ratio must be a positive float.
        """
        self.scale_to(self.scale + ratio)

    def scaled_size(self):
        """return the sprite's calculated size, after scaling
        """
        (width, height) = self.original.get_size()
        width = (int)(width * self.scale)
        height = (int)(height * self.scale)
        return (width, height)

    @call_hook_method('on_visual_change')
    def rotate_to(self, degree):
        """rotate sprite's image by a degree (overwriting)
        """
        self.rotate = degree % 360  # TODO magic number?
        self.update_image()

    @call_hook_method('on_visual_change')
    def rotate_by(self, degree):
        """ rotate sprite's image by a degree (accumalating)
        """
        self.rotate_to(self.rotate + degree)

    def add(self, *groups):
        """add the sprite to groups

        Sprite.add(*groups): return None

        Any number of Group instances can be passed as arguments. The
        Sprite will be added to the Groups it is not already a member of.

        """
        has = self.__g.__contains__
        for group in groups:
            if hasattr(group, '_spritegroup'):
                if not has(group):
                    group.add_internal(self)
                    self.add_internal(group)
            else:
                self.add(*group)

    def remove(self, *groups):
        """remove the sprite from groups

        Sprite.remove(*groups): return None

        Any number of Group instances can be passed as arguments. The Sprite
        will be removed from the Groups it is currently a member of.

        """
        has = self.__g.__contains__
        for group in groups:
            if hasattr(group, '_spritegroup'):
                if has(group):
                    group.remove_internal(self)
                    self.remove_internal(group)
            else:
                self.remove(*group)

    def add_internal(self, group):
        self.__g[group] = 0

    def remove_internal(self, group):
        del self.__g[group]

    def update(self, *args):
        """method to control sprite behavior

        Sprite.update(*args):

        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override. This method is called by
        Group.update() with whatever arguments you give it.

        There is no need to use this method if not using the convenience
        method by the same name in the Group class.

        """
        pass

    def kill(self):
        """remove the Sprite from all Groups

        Sprite.kill(): return None

        The Sprite is removed from all the Groups that contain it. This won't
        change anything about the state of the Sprite. It is possible to
        continue to use the Sprite after this method has been called, including
        adding it to Groups.

        """
        for c in self.__g:
            c.remove_internal(self)
        self.__g.clear()

    def groups(self):
        """list of Groups that contain this Sprite

        Sprite.groups(): return group_list

        Returns a list of all the Groups that contain this Sprite.

        """
        return list(self.__g)

    def alive(self):
        """does the sprite belong to any groups

        Sprite.alive(): return bool

        Returns True when the Sprite belongs to one or more Groups.
        """
        return truth(self.__g)

    def __repr__(self):
        return "<%s sprite(in %d groups)>" \
            % (self.__class__.__name__, len(self.__g))


class AggregatedSprite(Sprite):
    """aggregated sprite class collects many sprites into single entity

    pygame.sprite.AggregatedSprite(*groups): return AggregatedSprite

    The aggregated sprite holds a list of child sprites and propagates
    every visual change to all of the child sprites.
    """
    def __init__(self, *groups):
        """iniitalizes sprite
        """
        # call super's initialization as usual.
        super(AggregatedSprite, self).__init__(*groups)
        # reset sprites list
        self.sprites = []
        # resets the rect and position which would be calculated
        # according to added sprite.
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.position = (0, 0)

    def add_sprite(self, sprite):
        """add a sprite to the list of child sprites
        """
        self.sprites.append(sprite)

    def draw(self, surface):
        """draw child sprites in order

        AggregatedSprite.draw(surface): return Rect

        Returns a rectangle that is the union of all
        child sprites' rects.
        """
        #TODO consider sprite's layer attribute
        ret = pygame.Rect(0, 0, 0, 0)
        for spr in self.sprites:
            r = spr.draw(surface)
            if r != 0:
                ret.union_ip(r)
        return ret

    def on_visual_change(self, method, *args, **kwargs):
        """propagate a visual attribute change to all child sprites
        """
        super(AggregatedSprite, self).on_visual_change(method, *args, **kwargs)
        if method.__name__ == 'move_to':
            for spr in self.sprites:
                spr.set_offset(args[0])
        else:
            for spr in self.sprites:
                method(spr, *args, **kwargs)
            if method.__name__ == 'move_by':
                return False
        return True


class AbstractGroup(object):
    """base class for containers of sprites

    AbstractGroup does everything needed to behave as a normal group. You can
    easily subclass a new group class from this or the other groups below if
    you want to add more features.

    Any AbstractGroup-derived sprite groups act like sequences and support
    iteration, len, and so on.

    """

    # dummy val to identify sprite groups, and avoid infinite recursion
    _spritegroup = True

    def __init__(self):
        self.spritedict = {}
        self.lostsprites = []

    def sprites(self):
        """get a list of sprites in the group, ordered by layer

        Group.sprites(): return list

        Returns an object that can be looped over with a 'for' loop. (For now,
        it is always a list, but this could change in a future version of
        pygame.) Alternatively, you can get the same information by iterating
        directly over the sprite group, e.g. 'for sprite in group'.
        """
        return sorted(self.spritedict,
                      key=lambda sprite: getattr(sprite, "layer", 0))

    def add_internal(self, sprite):
        self.spritedict[sprite] = 0

    def remove_internal(self, sprite):
        r = self.spritedict[sprite]
        if r is not 0:
            self.lostsprites.append(r)
        del self.spritedict[sprite]

    def has_internal(self, sprite):
        return sprite in self.spritedict

    def copy(self):
        """copy a group with all the same sprites

        Group.copy(): return Group

        Returns a copy of the group that is an instance of the same class
        and has the same sprites in it.

        """
        return self.__class__(self.sprites())

    def __iter__(self):
        return iter(self.sprites())

    def __contains__(self, sprite):
        return self.has(sprite)

    def add(self, *sprites):
        """add sprite(s) to group

        Group.add(sprite, list, group, ...): return None

        Adds a sprite or sequence of sprites to a group.

        """
        for sprite in sprites:
            # It's possible that some sprite is also an iterator.
            # If this is the case, we should add the sprite itself,
            # and not the iterator object.
            if isinstance(sprite, Sprite):
                if not self.has_internal(sprite):
                    self.add_internal(sprite)
                    sprite.add_internal(self)
            else:
                try:
                    # See if sprite is an iterator, like a list or sprite
                    # group.
                    self.add(*sprite)
                except (TypeError, AttributeError):
                    # Not iterable. This is probably a sprite that is not an
                    # instance of the Sprite class or is not an instance of a
                    # subclass of the Sprite class. Alternately, it could be an
                    # old-style sprite group.
                    if hasattr(sprite, '_spritegroup'):
                        for spr in sprite.sprites():
                            if not self.has_internal(spr):
                                self.add_internal(spr)
                                spr.add_internal(self)
                    elif not self.has_internal(sprite):
                        self.add_internal(sprite)
                        sprite.add_internal(self)

    def remove(self, *sprites):
        """remove sprite(s) from group

        Group.remove(sprite, list, or group, ...): return None

        Removes a sprite or sequence of sprites from a group.

        """
        # This function behaves essentially the same as Group.add. It first
        # tries to handle each argument as an instance of the Sprite class. If
        # that failes, then it tries to handle the argument as an iterable
        # object. If that failes, then it tries to handle the argument as an
        # old-style sprite group. Lastly, if that fails, it assumes that the
        # normal Sprite methods should be used.
        for sprite in sprites:
            if isinstance(sprite, Sprite):
                if self.has_internal(sprite):
                    self.remove_internal(sprite)
                    sprite.remove_internal(self)
            else:
                try:
                    self.remove(*sprite)
                except (TypeError, AttributeError):
                    if hasattr(sprite, '_spritegroup'):
                        for spr in sprite.sprites():
                            if self.has_internal(spr):
                                self.remove_internal(spr)
                                spr.remove_internal(self)
                    elif self.has_internal(sprite):
                        self.remove_internal(sprite)
                        sprite.remove_internal(self)

    def has(self, *sprites):
        """ask if group has a sprite or sprites

        Group.has(sprite or group, ...): return bool

        Returns True if the given sprite or sprites are contained in the
        group. Alternatively, you can get the same information using the
        'in' operator, e.g. 'sprite in group', 'subgroup in group'.

        """
        return_value = False

        for sprite in sprites:
            if isinstance(sprite, Sprite):
                # Check for Sprite instance's membership in this group
                if self.has_internal(sprite):
                    return_value = True
                else:
                    return False
            else:
                try:
                    if self.has(*sprite):
                        return_value = True
                    else:
                        return False
                except (TypeError, AttributeError):
                    if hasattr(sprite, '_spritegroup'):
                        for spr in sprite.sprites():
                            if self.has_internal(spr):
                                return_value = True
                            else:
                                return False
                    else:
                        if self.has_internal(sprite):
                            return_value = True
                        else:
                            return False

        return return_value

    def update(self, *args):
        """call the update method of every member sprite

        Group.update(*args): return None

        Calls the update method of every member sprite. All arguments that
        were passed to this method are passed to the Sprite update function.

        """
        for s in self.sprites():
            s.update(*args)

    def draw(self, surface):
        """draw all sprites onto the surface

        Group.draw(surface): return None

        Draws all of the member sprites onto the given surface.

        """
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            if (hasattr(spr, 'draw')):
                self.spritedict[spr] = spr.draw(surface)
            else:
                self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []

    def clear(self, surface, bgd):
        """erase the previous position of all sprites

        Group.clear(surface, bgd): return None

        Clears the area under every drawn sprite in the group. The bgd
        argument should be Surface which is the same dimensions as the
        screen surface. The bgd could also be a function which accepts
        the given surface and the area to be cleared as arguments.

        """
        if callable(bgd):
            for r in self.lostsprites:
                bgd(surface, r)
            for r in self.spritedict.values():
                if r is not 0:
                    bgd(surface, r)
        else:
            surface_blit = surface.blit
            for r in self.lostsprites:
                surface_blit(bgd, r, r)
            for r in self.spritedict.values():
                if r is not 0:
                    surface_blit(bgd, r, r)

    def empty(self):
        """remove all sprites

        Group.empty(): return None

        Removes all the sprites from the group.

        """
        for s in self.sprites():
            self.remove_internal(s)
            s.remove_internal(self)

    def __nonzero__(self):
        return truth(self.sprites())

    def __len__(self):
        """return number of sprites in group

        Group.len(group): return int

        Returns the number of sprites contained in the group.

        """
        return len(self.sprites())

    def __repr__(self):
        return "<%s(%d sprites)>" % (self.__class__.__name__, len(self))


class Group(AbstractGroup):
    """container class for many Sprites

    pygame.sprite.Group(*sprites): return Group

    A simple container for Sprite objects. This class can be subclassed to
    create containers with more specific behaviors. The constructor takes any
    number of Sprite arguments to add to the Group. The group supports the
    following standard Python operations:

        in      test if a Sprite is contained
        len     the number of Sprites contained
        bool    test if any Sprites are contained
        iter    iterate through all the Sprites

    The Sprites in the Group are not ordered, so the Sprites are drawn and
    iterated over in no particular order.

    """
    def __init__(self, *sprites):
        AbstractGroup.__init__(self)
        self.add(*sprites)

RenderPlain = Group
RenderClear = Group
