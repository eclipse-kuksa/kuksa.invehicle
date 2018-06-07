# AGL KUKSA

Kuksa is a wrapper project around Automotive Grade Linux (AGL). From its side,
AGL uses Yocto/Bitbake building system to build an automotive domain specific
Linux distribution. Therefore, this projects provides a building system that
adds Kuksa's specific Bitbake layers on top of the original AGL.

# Dependencies

To be able to build this AGL image first install the building dependencies by
running;

```
  apt install cmake curl chrpath build-essential texinfo
```

# Build the Image/SDK

To build the Image/SDK, run;

```
  cd <agl-kuksa-root>
  mkdir build
  cd build
  cmake ..
  make <agl-kuksa-target>
```

Where `<agl-kuksa-target>` can be;

* `agl-kuksa`: AGL kuksa image and SDK
* `agl-kuksa-config`: Configure AGL building environment for building agl-kuksa
* `agl-rover`: AGL Rover image and SDK
* `agl-rover-config`: Configure AGL building environment for building agl-rover

The output images can be seen at `<agl-kuksa-root>/build/images` and the SDKs at `<agl-kuksa-root>/build/sdk`.

# Documentation

The official documentation of this project can be reviewed [here](https://gitlab-pages.idial.institute/appstacle/agl-kuksa/index.html).
