# Unit 6: Working Together

## Creating agent dialogues

A KQML and KIF dialogue between Alice, an agent procuring stock, and Bob, an agent controlling a warehouse. Both use KIF as the content language and a shared warehouse-stock ontology. Stock figures are illustrative.

```
(ask-all  :sender alice :receiver bob :reply-with q1 :language KIF :ontology warehouse-stock
          :content (and (television ?m) (= (screen-size ?m) 50) (> (stock-level ?m) 0)))

(tell     :sender bob :receiver alice :in-reply-to q1 :language KIF :ontology warehouse-stock
          :content (and (television tv-50a) (= (screen-size tv-50a) 50) (= (stock-level tv-50a) 34)
                        (television tv-50b) (= (screen-size tv-50b) 50) (= (stock-level tv-50b) 6)))

(ask-one  :sender alice :receiver bob :reply-with q2 :language KIF :ontology warehouse-stock
          :content (= (hdmi-ports tv-50a) ?p))

(tell     :sender bob :receiver alice :in-reply-to q2 :language KIF :ontology warehouse-stock
          :content (= (hdmi-ports tv-50a) 4))

(ask-one  :sender alice :receiver bob :reply-with q3 :language KIF :ontology warehouse-stock
          :content (= (refresh-rate tv-50b) ?r))

(sorry    :sender bob :receiver alice :in-reply-to q3)

(achieve  :sender alice :receiver bob :reply-with q4 :language KIF :ontology warehouse-stock
          :content (reserved tv-50a 20 alice))

(tell     :sender bob :receiver alice :in-reply-to q4 :language KIF :ontology warehouse-stock
          :content (and (reserved tv-50a 20 alice) (= (stock-level tv-50a) 14)))
```

ask-all requests every binding of ?m; in-reply-to ties each answer to its question; sorry means Bob understood but has no answer, unlike error; achieve asks Bob to change the world rather than report on it. The exchange works only because both agents share the ontology, and KQML itself does not oblige Bob to answer or comply.

## Development Team Project

Group F submitted the design proposal for the Academic Evidence Investigator this unit. See [Final Project](final-project.html) and [Team Work](team.html).
