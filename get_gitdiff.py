sample_input=[
"Foo-v2/README",
"Foo-v2/meta.json",
"Bar-v1/meta.json",
"z-ctrl-target-server/ecommerce-mail.json,"
"z-ctrl-shared-flows/Ecommerce-OIDC-auth-v2/meta.json",
"z-ctrl-shared-flows/Ecommerce-OIDC-auth-v2/README.md"
]

def sanitize_diffs():
    to_split_input = [x.split("/") for x in sample_input if not x.startswith("z-ctrl-target-server/") and not x.startswith("z-ctrl-shared-flows/")]
    non_split_input= list(filter(lambda flow: flow.startswith("z-ctrl-shared-flows/") , sample_input))
    non_split_shared_flows=[x.split("/") for x in sample_input if x.startswith("z-ctrl-shared-flows/")]
    split_shared_flows=[sublist[1] for sublist in non_split_shared_flows]
    split_list = [sublist[0] for sublist in to_split_input]
    sample_output={*split_list,*non_split_input,*split_shared_flows}
    output_list=list(sample_output)
    return output_list
sanitize_diffs()


output=sanitize_diffs()
print(output)