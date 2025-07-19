function sanitizeSubject(subject) {
  return subject.trim().replace(/\s+/g, '_');
}

async function uploadPDF(options) {
  const { year, branch, subject, type, file } = options;
  if (!window.showDirectoryPicker) {
    alert('Your browser does not support the File System Access API.');
    return;
  }
  try {
    const root = await window.showDirectoryPicker();
    let dir = await root.getDirectoryHandle('sample_papers', { create: true });
    dir = await dir.getDirectoryHandle(branch, { create: true });
    dir = await dir.getDirectoryHandle(year, { create: true });
    dir = await dir.getDirectoryHandle(type, { create: true });
    const fileHandle = await dir.getFileHandle(sanitizeSubject(subject) + '.pdf', { create: true });
    const writable = await fileHandle.createWritable();
    await writable.write(await file.arrayBuffer());
    await writable.close();
    alert('PDF uploaded successfully!');
  } catch (err) {
    console.error(err);
    alert('Failed to upload PDF.');
  }
}

async function generateAndOpenPDF(options) {
  const { year, branch, subject, type, downloadLink } = options;
  const fileName = sanitizeSubject(subject) + '.pdf';
  const path = `sample_papers/${branch}/${year}/${type}/${fileName}`;
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error('Not found');
    if (downloadLink) {
      downloadLink.href = path;
      downloadLink.download = fileName;
      downloadLink.style.display = 'inline-block';
    }
    window.open(path, '_blank');
  } catch (err) {
    if (downloadLink) downloadLink.style.display = 'none';
    alert('PDF not found');
  }
}

window.QPF = { uploadPDF, generateAndOpenPDF, sanitizeSubject };
