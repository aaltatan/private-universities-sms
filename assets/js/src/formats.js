export function money(number) {
  let formattedNumber = number.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  let leftFormattedNumber = formattedNumber.padStart(15, " ");
  let rightFormattedNumber = formattedNumber.padEnd(15, " ");

  return `
  <pre class="rtl:hidden @max-lg:hidden font-extrabold">${leftFormattedNumber}</pre>
  <pre class="ltr:hidden @max-lg:hidden font-extrabold">${rightFormattedNumber}</pre>
  <pre class="@lg:hidden font-extrabold">${number}</pre>
  `;
}
