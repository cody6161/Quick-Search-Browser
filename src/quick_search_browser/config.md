# Quick Search Browser Configuration

`recent_added_days`

Number of days used by the `Recent Added` checkbox in the Browser.

Default:

```json
{
  "recent_added_days": 10
}
```

For example, setting this to `30` makes `Recent Added` search for cards added in
the last 30 days.

`yield_tags`

Maps each option in the `Yield` dropdown to the Anki tag that should be searched
when that option is selected.

Default:

```json
{
  "yield_tags": {
    "High Yield": "#AK_Step1_v12::#Low/HighYield::1-HighYield",
    "Relatively High Yield": "#AK_Step1_v12::#Low/HighYield::2-RelativelyHighYield",
    "High Yield Temporary": "#AK_Step1_v12::#Low/HighYield::3-HighYield-temporary",
    "Lower Yield": "#AK_Step1_v12::#Low/HighYield::4-LowerYield",
    "Low Yield": "#AK_Step1_v12::#Low/HighYield::5-LowYield"
  }
}
```

The text on the left is the dropdown label. The text on the right is the exact
tag searched with Anki's `tag:<tag>` search syntax.

Example: selecting `High Yield` searches for:

```text
tag:#AK_Step1_v12::#Low/HighYield::1-HighYield
```

If your cards use different tag names, change only the tag values on the right.
