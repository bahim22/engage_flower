#!/bin/bash

# || usr/bin/bash/

echo "VERCEL_ENV: $VERCEL_ENV"

if [[ "$VERCEL_ENV" == "production" ]] ; then
	echo "✅ | Proceed with the build"
	exit 1;

else
	echo "Do Not build | Build cancelled"
	exit 0;
fi