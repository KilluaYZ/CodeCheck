export interface MenuRoute {
	path: string;
	title?: string;
	name?: string;
	icon?: | string | { render: () => void };
	redirect?: string;
	children: MenuRoute[];
	meta: any
}

export type UserInfo = {
	userName: string,
	signature: string,
	userId: string,
	sex: string,
	email: string,
	avatar: string
}

export type UserAvatarList = {
	userHistoryFileList: Array<string>,
	systemAvatarList: Array<string>
};