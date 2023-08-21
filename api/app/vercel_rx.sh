#!/bin/bash

## #!/usr/bin/bash

echo "VERCEL_ENV: $VERCEL_ENV"

if [[
	"$VERCEL_ENV" == "production"
]] ; then
	echo "✔ - Proceed with Build"
	exit 1;

else
	echo "🚫 - Cancel Build"
	exit 0;
fi