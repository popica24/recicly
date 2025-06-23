(function ($) {
  "use strict";
  // Page loading
  $(window).on("load", function () {
    $("#preloader-active").delay(450).fadeOut("slow");
    $("body").delay(450).css({
      overflow: "visible",
    });
  });
  /*-----------------
        Menu Stick
    -----------------*/
  var header = $(".sticky-bar");
  var win = $(window);
  win.on("scroll", function () {
    var scroll = win.scrollTop();
    if (scroll < 50) {
      header.removeClass("stick");
    } else {
      header.addClass("stick");
    }
  });

  /*---------------------
        Mobile menu active
    ------------------------ */
  var $offCanvasNav = $(".mobile-menu"),
    $offCanvasNavSubMenu = $offCanvasNav.find(".dropdown");

  /*Add Toggle Button With Off Canvas Sub Menu*/
  $offCanvasNavSubMenu.parent().prepend('<span class="menu-expand">+</span>');

  /*Close Off Canvas Sub Menu*/
  $offCanvasNavSubMenu.slideUp();

  /*Category Sub Menu Toggle*/
  $offCanvasNav.on("click", "li a, li .menu-expand", function (e) {
    var $this = $(this);
    if (
      $this
        .parent()
        .attr("class")
        .match(/\b(menu-item-has-children|has-children|has-sub-menu)\b/) &&
      ($this.attr("href") === "#" || $this.hasClass("menu-expand"))
    ) {
      e.preventDefault();
      if ($this.siblings("ul:visible").length) {
        $this.parent("li").removeClass("active");
        $this.siblings("ul").slideUp();
      } else {
        $this.parent("li").addClass("active");
        $this
          .closest("li")
          .siblings("li")
          .removeClass("active")
          .find("li")
          .removeClass("active");
        $this.closest("li").siblings("li").find("ul:visible").slideUp();
        $this.siblings("ul").slideDown();
      }
    }
  });
})(jQuery);
