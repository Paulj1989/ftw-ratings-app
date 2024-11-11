# set plot theme
# inspired by https://github.com/z3tt/TidyTuesday/blob/main/R/2020_31_PalmerPenguins.Rmd

theme_ftw <- 
  function(
    base_size = 12, base_family = "Inter"
    ) {
    ggplot2::theme_minimal(
      base_size = base_size,
      base_family = base_family
      ) %+replace%
      ggplot2::theme(
        plot.background = ggplot2::element_rect(fill = "white", color = "white"),
        panel.grid.major = ggplot2::element_line(color = "grey90", linewidth = .4),
        panel.grid.minor = ggplot2::element_blank(),
        axis.title.x = ggplot2::element_text(
          color = "grey20", margin = ggplot2::margin(t = 10), size = ggplot2::rel(1.2)
          ),
        axis.title.y = ggplot2::element_text(
          color = "grey20", margin = ggplot2::margin(r = 10), size = ggplot2::rel(1.2)
          ),
        axis.text = ggplot2::element_text(color = "grey20", size = ggplot2::rel(1.1)),
        axis.text.y = ggplot2::element_text(
          colour = "grey20", size = ggplot2::rel(1.15), hjust = 0.5, lineheight = .4
          ),
        axis.ticks = ggplot2::element_line(color = "grey90", linewidth = .4),
        axis.ticks.y = ggplot2::element_blank(),
        axis.ticks.length = ggplot2::unit(.2, "lines"),
        legend.position = "top",
        legend.title = ggplot2::element_blank(),
        legend.text = ggplot2::element_text(
          size = ggplot2::rel(1.1), hjust = 0, margin = ggplot2::margin(0, 0, 0, 5)
          ),
        legend.spacing = ggplot2::unit(0, "cm"),
        legend.box.spacing = ggplot2::unit(0.5, "cm"),
        legend.key.width = ggplot2::unit(1, "cm"),
        plot.title = ggplot2::element_text(
          hjust = 0, color = "black",
          size = ggplot2::rel(2), margin = ggplot2::margin(t = 5, b = 5)
          ),
        plot.subtitle = ggplot2::element_text(
          hjust = 0, color = "grey30",
          lineheight = 0.8, size = ggplot2::rel(1.2),
          margin = ggplot2::margin(10, 0, 10, 0)
          ),
        plot.title.position = "plot",
        plot.caption = ggplot2::element_text(
          color = "grey50", size = ggplot2::rel(1.1), hjust = 1,
          margin = ggplot2::margin(15, 0, 0, 0)
          ),
        plot.caption.position = "plot",
        plot.margin = ggplot2::margin(rep(20, 4))
      )
    }