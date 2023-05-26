document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', event => {
        let target = event.target.closest('.select-search__trigger'),
            activeEl = document.activeElement;
        if (activeEl === target) {
            let searchList = event.target.closest('.select-search__trigger').nextElementSibling;
            window.addEventListener('keydown', event => {
                if ((event.which >= 65 && event.which <=90 || event.which == 186 || event.which == 222
                    || event.which == 188 || event.which == 190 || event.which == 219 || event.which == 221 || event.which == 192) && event.target === target) {
                    let suitableArray = [];
                    searchList.querySelectorAll('li label').forEach(item => {
                        item.style.cssText = 'color: #000';
                        if (item.textContent.slice(0,1).toLowerCase() == event.key) {
                            suitableArray.push(item);
                        }
                    });
                    if (suitableArray.length > 0) {
                        let scrollTargetEl = suitableArray[0];
                        scrollTargetEl.style.cssText = 'color: #b7b7b7';
                        window.scrollTo(0,0);
                        scrollTargetEl.scrollIntoView(false);
                    }
                    searchList.querySelectorAll('li label').forEach(item => {
                        item.addEventListener('mouseover', () => {
                            if (suitableArray.length > 0) {
                                suitableArray[0].style.cssText = 'color: #000';
                            }
                            item.style.cssText = 'color: #b7b7b7';
                        });
                        item.addEventListener('mouseout', () => {
                            item.style.cssText = 'color: #000';
                        });
                    });
                }
            });
        }
    })
});