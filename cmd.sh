set -x

npx md-to-pdf $2 --css "h3, h4 {color: #ac0303;}" --pdf-options "{\"format\":\"A4\",\"margin\":\"20mm\",\"printBackground\":true}" --highlight-style github $1/README.md
