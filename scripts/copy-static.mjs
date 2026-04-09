import { copyFileSync, mkdirSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = dirname(fileURLToPath(import.meta.url))
const out = join(root, '..', 'dist')
mkdirSync(out, { recursive: true })
copyFileSync(join(root, '..', 'public', 'index.html'), join(out, 'index.html'))
