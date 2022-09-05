## sha256
```
python sha256.py <option> <arguments>
```
### options
-c: compute hash of a given file
```
> python sha256.py -c greeting.txt 
e6c1396639c0b79bebc94e4448cfe2700b871d45d0d38d98df6ee9da3f09d35c
```

-v: verify a given hash of the specific file
```
> python sha256.py -v greeting.txt e6c1396639c0b79bebc94e4448cfe2700b871d45d0d38d98df6ee9da3f09d35c
True
```
