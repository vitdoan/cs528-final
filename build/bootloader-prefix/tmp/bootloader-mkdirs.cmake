# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/Users/reeyee/esp/esp-idf/components/bootloader/subproject"
  "/Users/reeyee/Documents/cs528/Assignment2/build/bootloader"
  "/Users/reeyee/Documents/cs528/Assignment2/build/bootloader-prefix"
  "/Users/reeyee/Documents/cs528/Assignment2/build/bootloader-prefix/tmp"
  "/Users/reeyee/Documents/cs528/Assignment2/build/bootloader-prefix/src/bootloader-stamp"
  "/Users/reeyee/Documents/cs528/Assignment2/build/bootloader-prefix/src"
  "/Users/reeyee/Documents/cs528/Assignment2/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/Users/reeyee/Documents/cs528/Assignment2/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/Users/reeyee/Documents/cs528/Assignment2/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
