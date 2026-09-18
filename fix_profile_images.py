import os

root = None
for entry in os.scandir('C:\\Users\\aDMIN'):
    if 'OneDrive' in entry.name:
        test = os.path.join(entry.path, 'Desktop', 'restaurant', 'Project-scholarship')
        if os.path.exists(os.path.join(test, 'backend', 'app', 'config.py')):
            root = test
            break

p = os.path.join(root, 'frontend', 'app', 'pages', 'profile.vue')
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add resolveImageUrl helper function before formatCurrency
old_marker = "const formatCurrency = (amount: number) => {"
new_marker = """const resolveImageUrl = (imagePath?: string) => {
  if (!imagePath) return ''
  if (imagePath.startsWith('http')) return imagePath
  return `${config.public.apiBase}${imagePath}`
}

const formatCurrency = (amount: number) => {"""
content = content.replace(old_marker, new_marker, 1)

# 2. Replace ALL occurrences of :src="item.product_image" with :src="resolveImageUrl(item.product_image)"
count = content.count(':src="item.product_image"')
content = content.replace(':src="item.product_image"', ':src="resolveImageUrl(item.product_image)"')

print(f'Replaced {count} image src occurrences')

# 3. Verify config is available
print('config available:', 'const config = useRuntimeConfig()' in content)
print('resolveImageUrl defined:', 'const resolveImageUrl' in content)
print('resolveImageUrl used:', 'resolveImageUrl(item.product_image)' in content)
print('No plain item.product_image src:', ':src="item.product_image"' not in content)

with open(p, 'w', encoding='utf-8') as f:
    f.write(content)

print('profile.vue updated successfully')
