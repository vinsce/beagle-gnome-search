suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def humanize_size(size_bytes):
	if size_bytes == 0: return '0 B'
	i = 0
	while size_bytes >= 1024 and i < len(suffixes) - 1:
		size_bytes /= 1024.
		i += 1
	f = ('%.2f' % size_bytes).rstrip('0').rstrip('.')
	return '%s %s' % (f, suffixes[i])