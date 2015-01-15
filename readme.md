# Usage

## http://www.timeanddate.com/

Note: Country names are typically lower case, and either hyphenated or acronymed if multiple words.  'the' and 'republic' and possibly other common words are discarded.

### Usage

```bash
scrapy timeanddate_com -a country=COUNTRY [ -a out=FILENAME ]
```

If `out` is not specified or is `-`, writes the result to stdout.  Otherwise, the result is written to the specified file.

