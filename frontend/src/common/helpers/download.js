export const resolveBlob = (response) => {
    const headerval = response.headers['content-disposition'];
    if (headerval != null) {
      let filename = headerval.split(';')[1].split('=')[1].replace('"', '').replace('"', '');
      filename = decodeURI(filename);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(url);
      link.remove();
    } else {
      handleKnownException(response);
    }
  }