# The Skeleton Key (200 PTS)
### Description
> Find the flag :)

Flag: ```SharifCTF{be278492ae9b998eaebe3ca54c8000de}```

### Files

- [The Skeleton Key.apk](The%20Skeleton%20Key.apk)

### Solution
 That's an ```.apk``` file, right? So we can just look inside as in ```zip archive```. 
 
 ```
C:\Users\Vova\Desktop\SharifCTF8> 7z.exe l "The Skeleton Key.apk"
7-Zip 18.01 (x64) : Copyright (c) 1999-2018 Igor Pavlov : 2018-01-28

Scanning the drive for archives:
1 file, 1106760 bytes (1081 KiB)
Listing archive: The Skeleton Key.apk
--
Path = The Skeleton Key.apk
Type = zip
Physical Size = 1106760

   Date      Time    Attr         Size   Compressed  Name
------------------- ----- ------------ ------------  ------------------------
2016-12-11 22:49:44 .....         1852          701  AndroidManifest.xml
2016-12-11 22:49:44 .....        28488         4575  assets\logo.svg
2016-12-11 22:49:44 .....          396          219  res\anim\abc_fade_in.xml
2016-12-11 22:49:44 .....          396          220  res\anim\abc_fade_out.xml
...
2016-12-11 22:49:44 .....      2114044       666605  classes.dex
2016-12-11 22:49:44 .....        31057         8839  META-INF\MANIFEST.MF
2016-12-11 22:49:44 .....        31086         8882  META-INF\CERT.SF
2016-12-11 22:49:44 .....         1107         1034  META-INF\CERT.RSA
------------------- ----- ------------ ------------  ------------------------
2016-12-11 22:49:44            2622145      1051454  297 files
C:\Users\Vova\Desktop\SharifCTF8>
```

A little spoiler: source code doesn't contain something unexpected, so let's look at ```assets\logo.svg```.

```
C:\Users\Vova\Desktop\SharifCTF8> 7z.exe e "The Skeleton Key.apk" assets\logo.svg
```

It's a skull!

<p><img src='images/skull.png' /></p>

But we need to look a bit closer. SVG document contains two ```<g>``` tags, first of them describes a skull image, second contains a lot of small coordinates. It's extremely small so we need to scale it up to see.

```
<g transform="matrix(0.97613485,-0.21716528,0.21716528,0.97613485,0,0)" style="..." id="text4146">
    <path d="m 450.04001,835.49603 q 0,0.009 ..." style="" id="path4388" />
    <path d="m 450.11496,835.49774 -0.0502,0 q ..." style="" id="path4390" />
    <path d="m 450.19241,835.53064 -0.0615,0 ..." style="" id="path4392" />
    <path d="m 450.27225,835.45337 -0.0411,0.0773 ..." style="" id="path4394" />
    <path d="m 450.35226,835.50531 q 0,0.0118 ..." style="" id="path4396" />
    ...
```

```450.xxxxx``` and ```835.xxxxx``` looks like X and Y coordinates, and other numbers are using to draw a picture. 
How we can zoom it? Use ```transform``` attribute! Just scale it by 200 times and translate to original position.

```
transform="scale(200, 200) translate(-448.75120, -834.69252)"
```

Save changes, re-open svg and...

<p><img src='images/scaled.png' /></p>
