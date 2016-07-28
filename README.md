# Extended Content Reader

**Copyright (c) 2016 David Betz**

## Purpose

Files have content and metadata. Markdown has already helps us go from boring text files to rich text (without RTF or proprietary voodoo), but it's still not enough for me. My content needs sections and it needs metadata. They already have a create date and a modified date, but I often need to overwrite these. That's where this simply component has been helping me for a few years now (well, this is the Python refactor/port of my original/production/more complex .NET version).

It's easier to following if you just look at the example...

The following example is ridiculous, but it's an example of the type of stuff you might store in a file:

**item01.txt**

    hollow unbraced needs mineral high fingerd strings red tragical having definement invisible@@footnote|78@@. flames grow pranks obey hearsed variable grandsire bodykins possessd worser oerthrown oerweigh healthful kingly wise faculty loggats best.

    unfortified chopine hill witchcraft countries toward nerve grief duty rivals.

    @@begin|format:javascript@@
        alert((function() {
          var item = 'item01';
          return item.split('').reverse();
        })());
    @@end@@

    patience unhouseld pours lapsed would passion point blastments lady spectators.

    @author@ Billy Speareshakes
    @title@ Thy Wonderful Randomious
    @page@ 728
    @footnote|78@ nose thee something disclaiming wrung antiquity rend illume halt osric list

There are two paragraphs, followed by a block of JavaScript, then another paragraph, then a bunch of metadata. It's a rediclous example because it combines concepts from both research website (citations and footnotes) and my [netfxharmonics.com](netfxharmonics.com) website (the javascript section, which in that context in final rendering would be rendered with JavaScript colored syntax).

The current python project reads that file as the following object:

    {
        '_': {
            0: 'hollow unbraced needs mineral high fingerd strings red tragical having definement invisible@@footnote|78@@. flames grow pranks obey hearsed variable grandsire bodykins possessd worser oerthrown oerweigh healthful kingly wise faculty loggats best.
            
            unfortified chopine hill witchcraft countries toward nerve grief duty rivals.',

            1: {'_': "    alert((function() {\n      var item = 'item01';\n      return item.split('').reverse()\n    })());",
           'format': 'javascript'},

            2: 'patience unhouseld pours lapsed would passion point blastments lady spectators.',
        },
        'author': 'Billy Speareshakes',
        'title': 'Thy Wonderful Randomious',
        'page': '728',
        'footnote|78': 'nose thee something disclaiming wrung antiquity rend illume halt osric list',
        'created': '2016-07-27T19:38:10Z',
        'modified': '2016-07-27T19:38:10Z',
        'filename': 'item01.txt',
        'extension': 'txt',
        'basename': 'item01',
    }

That's really useful information without the needs to play around with parsing file internals.

The created, modified, filename, extension, and basename are read from the file metadata, but created and modified can be overwritten using @created@ and @modified@ tokens.

But, it's not just metadata. On my technical website, I require color syntax for various programming languages. Preformatting makes the code unreadable. So, I need sections(@@begin...@@/@@end@@. On my research website, I require extensive citations and footnotes. So, I need linkable content (@@XXXX@@).

Project is indented to be compatible with Python 2 and 3.

See test_read.py for usage.

# Use Cases

* one entry == blog entry
* one entry == one quote (with citation data)
* one entry == one podcast mp3; you would use something like @audio@ which would tell your custom system that this entry is describing that particular mp3