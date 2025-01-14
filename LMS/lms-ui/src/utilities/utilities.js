export function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


export function getImagePath(path) {
  return require("@/assets/" + path)
}



export function lengthValidation(input, min, max) {
  const inputValue = input.trim();
  if (inputValue.length >= min && inputValue.length <= max) {
    return true
  } else {
    return `length must be between ${min} and ${max} characters.`
  }
}


export function authorValidation(input) {
  const pattern = /^\d+(,\d+)*$/;
  if (pattern.test(input.trim())) {
    return true;
  } else {
    return 'Input must be in the format: number1,number2, ...,numberX(no spaces allowed)';
  }
}

export function passwordValidation(password) {
  const passwordRegex = /^[a-zA-Z0-9!"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~]+$/;
  if (password.length>= 4 && password.length <= 22) {
    if (passwordRegex.test(password)) {
      return true;
    } else {
      return "only alphabets, digits, and punctuation marks (excluding quotation marks) are allowed.";
    }
  }
  else {
    return "password must be between 4 and 22 characters."
  }
}


export function emailValidation(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (1 <= email.length <= 120) {
    if (emailRegex.test(email)) {
      return true
    }
    else {
      return "invalid email address."
    }
  } else {
    return 'email must be less than 120 characters.'
  }
}

export function pdfValidation(filePath) {
  if (typeof filePath !== 'string') {
    return "Invalid PDF name.";
  }
  const fileExtension = filePath.split('.').pop().toLowerCase();

  return fileExtension === 'pdf'? true:"Invalid PDF name.";
}


export function required(input) {
  if (typeof input === 'string') {
    return (!input || input.trim() === '') ? "This field is required." : true;
  } else if (typeof input === 'number') {
    return (input === null || input === undefined) ? "This field is required." : true;
  } else {
    return "This field is required.";
  }
}

export function imageValidation(filePath) {
  if (typeof filePath !== 'string') {
    return "Invalid Image name.";
  }

  const fileExtension = filePath.split('.').pop().toLowerCase();

  return ['jpg', 'jpeg', 'png'].includes(fileExtension)? true:"Image must be jpg,jpeg or png.";
}


export function nameValidation(name) {
  const nameRegex = /^[a-zA-Z]+$/;
  if (nameRegex.test(name)) {
    return true
  } else {
    return "only alphabets allowed."
  }
}
